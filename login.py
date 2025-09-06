import streamlit as st
import hashlib
from crud.usuarios import cadastrar_usuario, lembrar_senha, validar_email
from db import get_connection
import pymysql.cursors

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_login(email: str, senha: str) -> dict:
    """Verifica as credenciais do usuário"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("""
                SELECT id, empresa_id, nome, email, TIPO_USUARIO 
                FROM DP_USUARIOS 
                WHERE email = %s AND senha_hash = %s
            """, (email, hash_senha(senha)))
            usuario = cur.fetchone()
            return usuario
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        return None
    finally:
        conn.close()

def show_login():
    """Exibe o formulário de login"""
    st.title("🔐 Login - Controle de Despesas")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Cadastrar", "Esqueci a Senha"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if not email or not senha:
                    st.warning("Preencha todos os campos!")
                else:
                    usuario = verificar_login(email, senha)
                    if usuario:
                        st.session_state.logged_in = True
                        st.session_state.usuario = usuario
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Email ou senha incorretos!")
    
    with tab2:
        with st.form("cadastro_form"):
            st.subheader("Novo Cadastro")
            empresa_id = st.number_input("ID da Empresa", min_value=1, step=1, key="cad_empresa")
            nome = st.text_input("Nome Completo", key="cad_nome")
            email_cad = st.text_input("Email", key="cad_email")
            senha_cad = st.text_input("Senha", type="password", key="cad_senha")
            confirmar_senha = st.text_input("Confirmar Senha", type="password", key="cad_confirmar")
            submit_cad = st.form_submit_button("Cadastrar")
            
            if submit_cad:
                if not all([empresa_id, nome.strip(), email_cad.strip(), senha_cad, confirmar_senha]):
                    st.warning("Preencha todos os campos!")
                elif not validar_email(email_cad):
                    st.warning("Por favor, insira um email válido.")
                elif senha_cad != confirmar_senha:
                    st.warning("As senhas não coincidem!")
                else:
                    success = cadastrar_usuario(empresa_id, nome, email_cad, senha_cad, "comum")
                    if success:
                        st.success("Cadastro realizado com sucesso! Faça login para continuar.")
                    else:
                        st.error("Erro ao cadastrar. O email pode já estar em uso.")
    
    with tab3:
        st.subheader("Recuperar Senha")
        email_rec = st.text_input("Digite seu email", key="rec_email")
        if st.button("Enviar instruções", key="rec_btn"):
            if email_rec and validar_email(email_rec):
                lembrar_senha(email_rec)
            else:
                st.warning("Por favor, insira um email válido.")