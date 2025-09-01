import streamlit as st
from autenticar import autenticar
from crud.usuarios import cadastrar_usuario, lembrar_senha
import css

# ---------------------------
# Inicializa session_state
# ---------------------------
def _init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
    if "page" not in st.session_state:
        st.session_state.page = "login"

# ---------------------------
# Tela de login
# ---------------------------
def show_login():
    _init_session()
    css.local_css()
    
    st.title("🔐 Controle de Despesas - Login")

    # Cria três abas
    tab_login, tab_cadastrar, tab_recuperar = st.tabs(
        ["Entrar", "Cadastrar novo usuário", "Esqueci minha senha"]
    )

    # ------------------- Aba Entrar -------------------
    with tab_login:
        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            email = st.text_input("E-mail", key="login_email")
            senha = st.text_input("Senha", type="password", key="login_senha")

            if st.button("Entrar", key="btn_entrar"):
                usuario = autenticar(email, senha)
                if usuario:
                    st.session_state.usuario = usuario
                    st.session_state.logged_in = True
                    st.session_state.page = "menu"
                    st.success(f"Bem-vindo, {usuario['nome']}!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha inválidos.")

    # ------------------- Aba Cadastrar -------------------
    with tab_cadastrar:
        st.info("Preencha os dados para criar um novo usuário.")
        empresa_id = st.number_input("ID da Empresa", min_value=1, step=1, key="cadastrar_empresa_id")
        nome = st.text_input("Nome completo", key="cadastrar_nome")
        email_new = st.text_input("E-mail (novo usuário)", key="cadastrar_email")
        senha_new = st.text_input("Senha", type="password", key="cadastrar_senha")
        tipo_usuario = st.selectbox("Tipo de usuário", ["comum", "administrador"], key="cadastrar_tipo")

        if st.button("Cadastrar usuário", key="btn_cadastrar"):
            if not (empresa_id and nome and email_new and senha_new):
                st.warning("Preencha todos os campos.")
            else:
                ok = cadastrar_usuario(empresa_id, nome, email_new, senha_new, tipo_usuario)
                if ok:
                    st.success("Usuário cadastrado com sucesso. Faça login na aba 'Entrar'.")
                else:
                    st.error("Erro ao cadastrar usuário. Verifique logs ou conexão com o banco.")

    # ------------------- Aba Esqueci minha senha -------------------
    with tab_recuperar:
        st.info("Informe seu e-mail e a nova senha.")
        email_rec = st.text_input("E-mail cadastrado", key="rec_email")
        nova_senha = st.text_input("Nova senha", type="password", key="rec_nova_senha")

        if st.button("Redefinir senha", key="btn_recuperar"):
            if not (email_rec and nova_senha):
                st.warning("Preencha e-mail e nova senha.")
            else:
                ok = lembrar_senha(email_rec, nova_senha)
                if ok:
                    st.success("Senha redefinida. Faça login na aba 'Entrar'.")
                else:
                    st.error("E-mail não encontrado ou erro ao redefinir senha.")

# Alias para compatibilidade
def login():
    show_login()
