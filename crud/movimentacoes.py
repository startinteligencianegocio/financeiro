import streamlit as st
from db import get_connection
from datetime import date, datetime
from css import local_css

# -------------------------
# Helpers de data
# -------------------------
def parse_date_str(s: str):
    if not s or s.strip() == "":
        return None
    try:
        return datetime.strptime(s, "%d/%m/%Y").date()
    except:
        return None

def format_date(d):
    if d is None:
        return "-"
    if isinstance(d, (date, datetime)):
        return d.strftime("%d/%m/%Y")
    try:
        dt = datetime.strptime(str(d), "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except:
        return str(d)

# -------------------------
# Função principal
# -------------------------
def show():
    local_css()
    st.subheader("Movimentações")

    # Controle de edição e exclusão
    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None
    if "delete_id" not in st.session_state:
        st.session_state.delete_id = None

    # -------------------------
    # Carregar dados auxiliares
    # -------------------------
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id, descricao, tipo_receita_despesas FROM DP_TIPO_RECEITAS_DESPESAS")
    tipos = cur.fetchall() or []

    cur.execute("SELECT id, descricao FROM DP_SUBTIPO_REC_DESP")
    subtipos = cur.fetchall() or []

    cur.execute("SELECT id, razao_social FROM DP_FORNECEDORES")
    fornecedores = cur.fetchall() or []

    cur.execute("SELECT id, descricao FROM DP_FORMAS_PAGTO")
    formas = cur.fetchall() or []

    cur.close()
    conn.close()

    map_tipos = {f"{t['descricao']} ({t['tipo_receita_despesas']})": t["id"] for t in tipos}
    map_sub = {s['descricao']: s['id'] for s in subtipos}
    map_for = {f['razao_social']: f['id'] for f in fornecedores}
    map_pag = {p['descricao']: p['id'] for p in formas}

    # -------------------------
    # Valores para edição
    # -------------------------
    edit_mode = st.session_state.edit_id is not None
    if edit_mode:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM DP_MOVIMENTACOES WHERE id=%s", (st.session_state.edit_id,))
        mov = cur.fetchone()
        cur.close()
        conn.close()

        tipo_val = next((k for k,v in map_tipos.items() if v == mov["id_tipo_despesas"]), "")
        subtipo_val = next((k for k,v in map_sub.items() if v == mov["id_subtipo_despesas"]), "")
        fornecedor_val = next((k for k,v in map_for.items() if v == mov["id_fornecedor"]), "")
        forma_val = next((k for k,v in map_pag.items() if v == mov["id_forma_pagamento"]), "")
        valor_val = float(mov["valor"])
        data_lanc_val = format_date(mov["data_lancamento"])
        data_venc_val = format_date(mov["data_vencimento"])
        data_pag_val = format_date(mov["data_pagamento"])
    else:
        tipo_val = subtipo_val = fornecedor_val = forma_val = ""
        valor_val = 0.0
        data_lanc_val = data_venc_val = date.today().strftime("%d/%m/%Y")
        data_pag_val = ""

    # -------------------------
    # Formulário
    # -------------------------
    with st.form("form_mov", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            options_tipo = [""] + list(map_tipos.keys())
            index_tipo = 0 if not tipo_val else options_tipo.index(tipo_val)
            tipo = st.selectbox("Tipo", options_tipo, index=index_tipo)

            options_for = [""] + list(map_for.keys())
            index_for = 0 if not fornecedor_val else options_for.index(fornecedor_val)
            fornecedor = st.selectbox("Fornecedor", options_for, index=index_for)

            valor = st.number_input(
                "Valor (R$)",
                min_value=0.0,
                format="%.2f",
                step=0.01,
                value=float(valor_val)
            )
        with col2:
            options_sub = [""] + list(map_sub.keys())
            index_sub = 0 if not subtipo_val else options_sub.index(subtipo_val)
            subtipo = st.selectbox("SubTipo", options_sub, index=index_sub)

            options_pag = [""] + list(map_pag.keys())
            index_pag = 0 if not forma_val else options_pag.index(forma_val)
            forma = st.selectbox("Forma Pagamento", options_pag, index=index_pag)

            data_lanc_str = st.text_input("Data Lançamento (DD/MM/YYYY)", value=data_lanc_val)
        with col3:
            data_venc_str = st.text_input("Data Vencimento (DD/MM/YYYY)", value=data_venc_val)
            data_pag_str = st.text_input("Data Pagamento (DD/MM/YYYY) — opcional", value=data_pag_val)

        col_save, col_cancel = st.columns(2)
        submit = col_save.form_submit_button("✅ Salvar")
        cancel = col_cancel.form_submit_button("ℹ️ Cancelar")

        if cancel:
            st.session_state.edit_id = None
            st.rerun()

        if submit:
            if not tipo.strip() or not fornecedor.strip() or not forma.strip():
                st.error("Preencha todos os campos obrigatórios!")
            else:
                data_lanc = parse_date_str(data_lanc_str)
                data_venc = parse_date_str(data_venc_str)
                data_pag = parse_date_str(data_pag_str)

                if not data_lanc or not data_venc:
                    st.error("Datas inválidas. Use DD/MM/YYYY")
                else:
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        if edit_mode:
                            cur.execute("""
                                UPDATE DP_MOVIMENTACOES SET
                                id_tipo_despesas=%s, id_subtipo_despesas=%s, id_fornecedor=%s,
                                id_forma_pagamento=%s, data_lancamento=%s, data_vencimento=%s,
                                data_pagamento=%s, valor=%s, tipo_receita_despesas=%s
                                WHERE id=%s
                            """, (
                                map_tipos[tipo],
                                map_sub.get(subtipo) if subtipo.strip() != "" else None,
                                map_for[fornecedor],
                                map_pag[forma],
                                data_lanc,
                                data_venc,
                                data_pag,
                                valor,
                                tipo.split("(")[1][0],
                                st.session_state.edit_id
                            ))
                            st.success("✅ Movimentação atualizada!")
                            st.session_state.edit_id = None
                        else:
                            cur.execute("""
                                INSERT INTO DP_MOVIMENTACOES
                                (id_tipo_despesas, id_subtipo_despesas, id_fornecedor, id_forma_pagamento, id_usuario,
                                 data_lancamento, data_vencimento, data_pagamento, valor, tipo_receita_despesas)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """, (
                                map_tipos[tipo],
                                map_sub.get(subtipo) if subtipo.strip() != "" else None,
                                map_for[fornecedor],
                                map_pag[forma],
                                st.session_state.usuario["id"],
                                data_lanc,
                                data_venc,
                                data_pag,
                                valor,
                                tipo.split("(")[1][0]
                            ))
                            st.success("✅ Movimentação cadastrada!")
                        conn.commit()
                        cur.close()
                        conn.close()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar movimentação: {e}")

    # -------------------------
    # Listagem das movimentações
    # -------------------------
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.id, m.valor, m.data_lancamento, m.data_vencimento, m.data_pagamento,
               t.descricao as tipo_nome, s.descricao as sub_nome, f.razao_social, p.descricao as forma
        FROM DP_MOVIMENTACOES m
        LEFT JOIN DP_TIPO_RECEITAS_DESPESAS t ON t.id = m.id_tipo_despesas
        LEFT JOIN DP_SUBTIPO_REC_DESP s ON s.id = m.id_subtipo_despesas
        LEFT JOIN DP_FORNECEDORES f ON f.id = m.id_fornecedor
        LEFT JOIN DP_FORMAS_PAGTO p ON p.id = m.id_forma_pagamento
        ORDER BY m.data_lancamento DESC
    """)
    movs = cur.fetchall() or []
    cur.close()
    conn.close()

    for m in movs:
        with st.container():
            st.markdown(
                f"""
                <div class="card">
                    <b>{m['tipo_nome']} - {m['sub_nome'] or '-'}</b><br>
                    Fornecedor: {m['razao_social']} | Forma: {m['forma']}<br>
                    Valor: R$ {m['valor']:.2f} | Lanç: {format_date(m['data_lancamento'])} | 
                    Venc: {format_date(m['data_vencimento'])} | Pag: {format_date(m['data_pagamento'])}
                </div>
                """, unsafe_allow_html=True
            )

            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("✏️ Alterar", key=f"edit_{m['id']}"):
                    st.session_state.edit_id = m["id"]
                    st.rerun()
            with col2:
                if st.session_state.delete_id == m["id"]:
                    # Exibe botões de confirmação
                    col_c1, col_c2 = st.columns([1,1])
                    with col_c1:
                        if st.button("✅ Confirmar", key=f"confirm_{m['id']}"):
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("DELETE FROM DP_MOVIMENTACOES WHERE id=%s", (m["id"],))
                            conn.commit()
                            cur.close()
                            conn.close()
                            st.success("Movimentação excluída!")
                            st.session_state.delete_id = None
                            st.rerun()
                    with col_c2:
                        if st.button("❌ Cancelar", key=f"cancel_{m['id']}"):
                            st.session_state.delete_id = None
                            st.rerun()
                else:
                    if st.button("🗑️ Excluir", key=f"del_{m['id']}"):
                        st.session_state.delete_id = m["id"]
                        st.rerun()
