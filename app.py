import streamlit as st
import login
import dashboard
import crud.fornecedores as fornecedores
import crud.tipos as tipos
import crud.subtipos as subtipos
import crud.formas_pagto as formas
import crud.movimentacoes as movs

st.set_page_config(page_title="Controle de Despesas", layout="wide")

# Topbar com usuário e logout
def topbar():
    left, right = st.columns([6, 4])
    with right:
        if st.session_state.get("usuario"):
            u = st.session_state.usuario
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**👤 {u['nome']}**")
            if c2.button("🚪 Logout"):
                st.session_state.clear()
                st.rerun()

if not st.session_state.get("logged_in"):
    login.show_login()
    st.stop()

# Autenticado:
topbar()
st.sidebar.title("📌 Menu")
opt = st.sidebar.radio("Navegação", [
    "Dashboard", "Fornecedores", "Tipos Desp / Rec",
    "Sub-Tipos Desp / Rec", "Formas de Pagamento", "Movimentações", "Usuários"
])

if opt == "Dashboard":
    # compatível com dashboard.show() OU dashboard.show_dashboard()
    if hasattr(dashboard, "show"):
        dashboard.show()
    else:
        dashboard.show_dashboard()
elif opt == "Fornecedores":
    fornecedores.show()
elif opt == "Tipos Desp / Rec":
    tipos.show()
elif opt == "Sub-Tipos Desp / Rec":
    subtipos.show()
elif opt == "Formas de Pagamento":
    formas.show()
elif opt == "Movimentações":
    movs.show()
elif opt == "Usuários":
    import crud.usuarios as usuarios
    usuarios.usuarios_page() if hasattr(usuarios, "usuarios_page") else st.info("Abra o módulo de usuários.")