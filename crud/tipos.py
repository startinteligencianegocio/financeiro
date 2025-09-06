import streamlit as st
from db import get_connection
from css import local_css
import pymysql

def show():
    local_css()
    st.subheader("Cadastro de Tipos de Receitas/Despesas")

    # Formulário para inclusão de novo tipo
    with st.form("form_tipo", clear_on_submit=True):
        desc = st.text_input("Descrição")
        tipo = st.selectbox("Tipo", ["R","D"])
        submit = st.form_submit_button("Salvar")
        if submit:
            if not desc:
                st.warning("Preencha a descrição!")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO DP_TIPO_RECEITAS_DESPESAS (descricao, tipo_receita_despesas) VALUES (%s,%s)",
                    (desc, tipo)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("Tipo cadastrado com sucesso!")
                st.rerun()

    st.write("### Lista de Tipos Rec/Desp.")

    # Buscar tipos do banco
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)  # resultados como dicionário
    cur.execute("SELECT * FROM DP_TIPO_RECEITAS_DESPESAS ORDER BY id")
    tipos = cur.fetchall()
    cur.close()
    conn.close()

    # Loop para exibir cada tipo
    for t in tipos:
        if f"edit_{t['id']}" not in st.session_state:
            st.session_state[f"edit_{t['id']}"] = False  # flag de edição

        col1, col2, col3, col4 = st.columns([3,1,1,1])
        col1.write(t["descricao"])
        col2.write(t["tipo_receita_despesas"])

        # Botão Alterar
        if col3.button("Alterar", key=f"alt_tipo_{t['id']}"):
            st.session_state[f"edit_{t['id']}"] = True
            st.rerun()

        # Botão Excluir
        if col4.button("Excluir", key=f"del_tipo_{t['id']}"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM DP_TIPO_RECEITAS_DESPESAS WHERE id=%s", (t["id"],))
            conn.commit()
            cur.close()
            conn.close()
            st.success("Tipo excluído!")
            st.rerun()

        # Se estiver em modo edição, mostrar inputs
        if st.session_state[f"edit_{t['id']}"]:
            novo_desc = st.text_input("Nova Descrição", t["descricao"], key=f"desc_{t['id']}")
            novo_tipo = st.selectbox(
                "Novo Tipo",
                ["R","D"],
                index=(0 if t["tipo_receita_despesas"]=="R" else 1),
                key=f"tipo_{t['id']}"
            )
            if st.button("Salvar Alterações", key=f"save_tipo_{t['id']}"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE DP_TIPO_RECEITAS_DESPESAS SET descricao=%s, tipo_receita_despesas=%s WHERE id=%s",
                    (novo_desc, novo_tipo, t["id"])
                )
                conn.commit()
                cur.close()
                conn.close()
                st.session_state[f"edit_{t['id']}"] = False
                st.success("Tipo atualizado!")
                st.rerun()
