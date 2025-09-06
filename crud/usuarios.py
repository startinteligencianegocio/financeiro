import streamlit as st
import hashlib
import re
from db import get_connection
from css import local_css
import pymysql.cursors

local_css()

# ---------------------------
# Hash de senha
# ---------------------------
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# ---------------------------
# Função lembrar_senha (nova)
# ---------------------------
def lembrar_senha(email: str) -> bool:
    """
    Envia email para redefinição de senha (implementação básica)
    Na prática, você integraria com um serviço de email
    """
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Verifica se o email existe
            cur.execute("SELECT id FROM DP_USUARIOS WHERE email = %s", (email,))
            usuario = cur.fetchone()
            
            if usuario:
                # Aqui você implementaria o envio de email real
                st.info(f"Instruções para redefinir senha foram enviadas para {email}")
                return True
            else:
                st.warning("Email não encontrado no sistema.")
                return False
    except Exception as e:
        print(f"Erro ao processar lembrar senha: {e}")
        return False
    finally:
        conn.close()

# ---------------------------
# Função de validação de email
# ---------------------------
def validar_email(email: str) -> bool:
    """Valida formato do email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ---------------------------
# Usuários Page
# ---------------------------
def usuarios_page():
    st.subheader("Gestão de Usuários")

    conn = get_connection()
    if not conn:
        st.error("Não foi possível conectar ao banco de dados.")
        return

    try:
        # Cursor como dict
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM DP_USUARIOS ORDER BY id")
            usuarios = cur.fetchall()
    except Exception as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return
    finally:
        conn.close()

    # --- Formulário para inclusão de usuário ---
    st.write("### Cadastrar Novo Usuário")
    with st.form("form_novo_usuario", clear_on_submit=True):
        empresa_id = st.number_input("ID da Empresa", min_value=1, step=1)
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        tipo_usuario = st.selectbox("Tipo de Usuário", ["comum", "administrador"])
        submit = st.form_submit_button("Salvar")

        if submit:
            if not nome.strip() or not email.strip() or not senha.strip():
                st.warning("Preencha todos os campos!")
            elif not validar_email(email):
                st.warning("Por favor, insira um email válido.")
            else:
                success = cadastrar_usuario(empresa_id, nome, email, senha, tipo_usuario)
                if success:
                    st.success("Usuário cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao cadastrar usuário. Verifique se o email já existe.")

    # --- Listagem e edição ---
    st.write("### Usuários Cadastrados")
    for u in usuarios:
        if f"edit_{u['id']}" not in st.session_state:
            st.session_state[f"edit_{u['id']}"] = False

        col1, col2, col3, col4 = st.columns([2,2,1,1])

        # Modo de edição
        if st.session_state[f"edit_{u['id']}"]:
            novo_nome = col1.text_input("Nome", value=u["nome"], key=f"nome_{u['id']}")
            novo_email = col2.text_input("Email", value=u["email"], key=f"email_{u['id']}")
            novo_tipo = col3.selectbox(
                "Tipo",
                ["comum", "administrador"],
                index=(0 if u["TIPO_USUARIO"]=="comum" else 1),
                key=f"tipo_{u['id']}"
            )
            if col4.button("Salvar", key=f"save_{u['id']}"):
                if validar_email(novo_email):
                    editar_usuario(u["id"], novo_nome, novo_email, novo_tipo)
                    st.session_state[f"edit_{u['id']}"] = False
                    st.success("Usuário atualizado!")
                    st.rerun()
                else:
                    st.warning("Por favor, insira um email válido.")
        else:
            col1.write(u["nome"])
            col2.write(u["email"])
            col3.write(u["TIPO_USUARIO"])
            if col4.button("Alterar", key=f"editbtn_{u['id']}"):
                st.session_state[f"edit_{u['id']}"] = True
                st.rerun()
            if col4.button("Excluir", key=f"delbtn_{u['id']}"):
                excluir_usuario(u["id"])
                st.success("Usuário excluído!")
                st.rerun()

# ---------------------------
# Funções de CRUD (mantidas como estavam)
# ---------------------------
def cadastrar_usuario(empresa_id, nome, email, senha, tipo_usuario="comum") -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            senha_hash = hash_senha(senha)
            cur.execute("""
                INSERT INTO DP_USUARIOS (empresa_id, nome, email, senha_hash, TIPO_USUARIO, criado_em)
                VALUES (%s,%s,%s,%s,%s,NOW())
            """, (empresa_id, nome, email, senha_hash, tipo_usuario))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False
    finally:
        conn.close()

def editar_usuario(user_id, nome, email, tipo_usuario) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE DP_USUARIOS
                SET nome=%s, email=%s, TIPO_USUARIO=%s
                WHERE id=%s
            """, (nome, email, tipo_usuario, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao editar usuário: {e}")
        return False
    finally:
        conn.close()

def excluir_usuario(user_id) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM DP_USUARIOS WHERE id=%s", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return False
    finally:
        conn.close()

def redefinir_senha(email, nova_senha) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE DP_USUARIOS SET senha_hash=%s WHERE email=%s
            """, (hash_senha(nova_senha), email))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Erro ao redefinir senha: {e}")
        return False
    finally:
        conn.close()