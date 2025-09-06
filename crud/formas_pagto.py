import streamlit as st
from db import get_connection
from css import local_css
import pymysql

def show():
    local_css()
    st.subheader("Cadastro de Formas de Pagamento")

    # ===== FORMULÁRIO DE INCLUSÃO =====
    with st.form("form_pagto", clear_on_submit=True):
        desc = st.text_input("Descrição")
        submit = st.form_submit_button("Salvar")
        if submit:
            if desc.strip() == "":
                st.warning("Digite uma descrição antes de salvar.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO DP_FORMAS_PAGTO (descricao) VALUES (%s)",
                    (desc,)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("Forma cadastrada com sucesso!")
                st.rerun()

    # ===== LISTAGEM DE FORMAS =====
    st.write("### Lista de Formas de Pagamento")
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)  # resultados como dict
    cur.execute("SELECT * FROM DP_FORMAS_PAGTO ORDER BY id")
    formas = cur.fetchall()
    cur.close()
    conn.close()

    if "editando_forma" not in st.session_state:
        st.session_state["editando_forma"] = None

    # ===== LISTAGEM COM BOTÕES =====
    for f in formas:
        st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 1, 1])

        if st.session_state["editando_forma"] == f["id"]:
            # ===== MODO EDIÇÃO =====
            novo_desc = col1.text_input(
                "Nova Descrição", f["descricao"], key=f"desc_{f['id']}"
            )
            salvar = col2.button("Salvar Alterações", key=f"save_forma_{f['id']}")
            cancelar = col3.button("Cancelar", key=f"cancel_forma_{f['id']}")

            if salvar:
                if novo_desc.strip() == "":
                    st.warning("A descrição não pode ser vazia.")
                else:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE DP_FORMAS_PAGTO SET descricao=%s WHERE id=%s",
                        (novo_desc, f["id"])
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.session_state["editando_forma"] = None
                    st.success("Forma alterada com sucesso!")
                    st.rerun()

            if cancelar:
                st.session_state["editando_forma"] = None
                st.rerun()

        else:
            # ===== MODO NORMAL =====
            col1.write(f["descricao"])

            # Botão Alterar
            if col2.button("Alterar", key=f"alt_forma_{f['id']}"):
                st.session_state["editando_forma"] = f["id"]
                st.rerun()

            # Botão Excluir com verificação de integridade
            if col3.button("Excluir", key=f"del_forma_{f['id']}"):
                conn = get_connection()
                cur = conn.cursor()
                # Verifica se a forma está em uso
                cur.execute(
                    "SELECT COUNT(*) FROM DP_MOVIMENTACOES WHERE id_forma_pagamento=%s",
                    (f["id"],)
                )
                count = cur.fetchone()[0]
                if count > 0:
                    st.warning("Não é possível excluir esta forma de pagamento porque ela está sendo usada em movimentações.")
                else:
                    cur.execute(
                        "DELETE FROM DP_FORMAS_PAGTO WHERE id=%s",
                        (f["id"],)
                    )
                    conn.commit()
                    st.success("Forma excluída com sucesso!")
                cur.close()
                conn.close()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
