import streamlit as st
from db import get_connection
from css import local_css
import pymysql

def show():
    local_css()
    st.subheader("Cadastro de SubTipos de Receitas/Despesas")

    # --- Buscar tipos existentes ---
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM DP_TIPO_RECEITAS_DESPESAS")
    tipos = cur.fetchall()
    cur.close()
    conn.close()

    map_tipos = {f"{t['descricao']} ({t['tipo_receita_despesas']})": t["id"] for t in tipos}

    # --- Formulário para incluir novo subtipo ---
    with st.form("form_incluir_subtipo", clear_on_submit=True):
        desc = st.text_input("Descrição")
        tipo_escolhido = st.selectbox("Tipo", list(map_tipos.keys()))
        submit = st.form_submit_button("Salvar")
        if submit:
            if not desc:
                st.warning("Preencha a descrição antes de salvar.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO DP_SUBTIPO_REC_DESP (id_despesa, descricao) VALUES (%s,%s)",
                    (map_tipos[tipo_escolhido], desc)
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("SubTipo cadastrado com sucesso!")
                st.rerun()

    # --- Listar SubTipos existentes ---
    st.write("### Lista de SubTipos")
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("""
        SELECT s.id, s.descricao, t.descricao as tipo_nome, t.tipo_receita_despesas 
        FROM DP_SUBTIPO_REC_DESP s
        JOIN DP_TIPO_RECEITAS_DESPESAS t ON t.id = s.id_despesa
        ORDER BY s.id
    """)
    subs = cur.fetchall()
    cur.close()
    conn.close()

    for s in subs:
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        col1.write(s["descricao"])
        col2.write(f"{s['tipo_nome']} ({s['tipo_receita_despesas']})")

        # Botão Alterar
        if col3.button("Alterar", key=f"alt_sub_{s['id']}"):
            st.session_state["edit_sub_id"] = s["id"]
            st.session_state["edit_sub_desc"] = s["descricao"]
            st.rerun()

        # Botão Excluir
        if col4.button("Excluir", key=f"del_sub_{s['id']}"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM DP_SUBTIPO_REC_DESP WHERE id=%s", (s["id"],))
            conn.commit()
            cur.close()
            conn.close()
            st.success("SubTipo excluído com sucesso!")
            st.rerun()

    # --- Formulário de edição ---
    if "edit_sub_id" in st.session_state:
        st.write("### Alterar SubTipo")
        novo_desc = st.text_input(
            "Nova Descrição",
            value=st.session_state["edit_sub_desc"],
            key="edit_desc_input"
        )
        if st.button("Salvar Alterações"):
            if not novo_desc:
                st.warning("Preencha a descrição antes de salvar.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE DP_SUBTIPO_REC_DESP SET descricao=%s WHERE id=%s",
                    (novo_desc, st.session_state["edit_sub_id"])
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("SubTipo alterado com sucesso!")
                # Limpar sessão e recarregar
                del st.session_state["edit_sub_id"]
                del st.session_state["edit_sub_desc"]
                st.rerun()
