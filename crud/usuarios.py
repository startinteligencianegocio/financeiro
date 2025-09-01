import mysql.connector
from mysql.connector import Error
import hashlib

# ---------------------------
# Conexão com o banco
# ---------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="sua_senha",
            database="financeiro"
        )
        return conn
    except Error as e:
        print(f"Erro de conexão: {e}")
        return None

# ---------------------------
# Hash de senha
# ---------------------------
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# ---------------------------
# Cadastrar novo usuário
# ---------------------------
def cadastrar_usuario(empresa_id, nome, email, senha, tipo_usuario="comum"):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            senha_hash = hash_senha(senha)
            cursor.execute("""
                INSERT INTO usuarios (empresa_id, nome, email, senha_hash, tipo_usuario, criado_em)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (empresa_id, nome, email, senha_hash, tipo_usuario))
            conn.commit()
            return True
        except Error as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

# ---------------------------
# Lembrar senha (redefinir senha)
# ---------------------------
def lembrar_senha(email, nova_senha):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            senha_hash = hash_senha(nova_senha)
            cursor.execute("""
                UPDATE usuarios
                SET senha_hash = %s
                WHERE email = %s
            """, (senha_hash, email))
            conn.commit()
            return cursor.rowcount > 0  # True se atualizou
        except Error as e:
            print(f"Erro ao redefinir senha: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False
