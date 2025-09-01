import streamlit as st
from db import get_connection
from css import local_css  # Importa o css.py

def show():
    # Aplica CSS personalizado
    local_css()

    st.subheader("Cadastro de Fornecedores")

    # Formulário de cadastro
    with st.form("form_fornec", clear_on_submit=True):
        st.markdown("<h4 class='titulo-form'>Novo Fornecedor</h4>", unsafe_allow_html=True)
        nome = st.text_input("Razão Social", key="nome_cad")
        cnpj = st.text_input("CNPJ", key="cnpj_cad")
        submit = st.form_submit_button("Salvar", help="Cadastrar fornecedor")
        if submit:
            if nome.strip() == "" or cnpj.strip() == "":
                st.warning("Preencha todos os campos!")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO DP_FORNECEDORES (razao_social, cnpj) VALUES (%s,%s)",
                    (nome, cnpj)
                )
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Fornecedor cadastrado com sucesso!")
                st.rerun()

    st.write("---")
    st.write("### Lista de Fornecedores")

    # Buscar fornecedores
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DP_FORNECEDORES ORDER BY razao_social")
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()

    # Inicializa variáveis de sessão
    if "edit_fornecedor_id" not in st.session_state:
        st.session_state.edit_fornecedor_id = None
    if "edit_razao_social" not in st.session_state:
        st.session_state.edit_razao_social = ""
    if "edit_cnpj" not in st.session_state:
        st.session_state.edit_cnpj = ""

    # Lista com botões estilizados
    for f in fornecedores:
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        col1.markdown(f"<p class='texto-lista'>{f['razao_social']}</p>", unsafe_allow_html=True)
        col2.markdown(f"<p class='texto-lista'>{f['cnpj']}</p>", unsafe_allow_html=True)

        # Alterar
        if col3.button("Alterar", key=f"alt_forn_{f['id']}", help="Alterar fornecedor"):
            st.session_state.edit_fornecedor_id = f["id"]
            st.session_state.edit_razao_social = f["razao_social"]
            st.session_state.edit_cnpj = f["cnpj"]

        # Excluir
        if col4.button("Excluir", key=f"del_forn_{f['id']}", help="Excluir fornecedor"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM DP_FORNECEDORES WHERE id=%s", (f["id"],))
            conn.commit()
            cur.close()
            conn.close()
            st.success("Fornecedor excluído com sucesso!")
            st.rerun()

    # Formulário de edição
    if st.session_state.edit_fornecedor_id is not None:
        st.write("---")
        st.markdown("<h4 class='titulo-form'>Alterar Fornecedor</h4>", unsafe_allow_html=True)
        novo_nome = st.text_input("Novo Nome", st.session_state.edit_razao_social, key="nome_edit")
        novo_cnpj = st.text_input("Novo CNPJ", st.session_state.edit_cnpj, key="cnpj_edit")

        col_save, col_cancel = st.columns([1,1])
        with col_save:
            if st.button("Salvar Alterações", key="btn_save"):
                if novo_nome.strip() == "" or novo_cnpj.strip() == "":
                    st.warning("Preencha todos os campos!")
                else:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE DP_FORNECEDORES SET razao_social=%s, cnpj=%s WHERE id=%s",
                        (novo_nome, novo_cnpj, st.session_state.edit_fornecedor_id)
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("Fornecedor alterado com sucesso!")
                    st.session_state.edit_fornecedor_id = None
                    st.rerun()

        with col_cancel:
            if st.button("Cancelar", key="btn_cancel"):
                st.session_state.edit_fornecedor_id = None
                st.rerun()
