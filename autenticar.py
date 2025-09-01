import mysql.connector
from mysql.connector import Error
import hashlib

# ---------------------------
# Conexão com o banco
# ---------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="193.203.184.92",   # ou IP do servidor MySQL
            user="u576686179_start",
            password="IntNeg2025@!",
            database="u576686179_start"
        )
        return conn
    except Error as e:
        print(f"Erro de conexão: {e}")
        return None

# ---------------------------
# Gerar hash da senha
# ---------------------------
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# ---------------------------
# Função para autenticar usuário
# ---------------------------
def autenticar(email: str, senha: str):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            senha_hash = hash_senha(senha)
            cursor.execute("""
                SELECT u.id, u.nome, u.email, u.tipo_usuario, u.empresa_id, e.razao_social
                FROM  DP_USUARIOS u
                LEFT JOIN EMPRESA e ON u.empresa_id = e.CODIGO
                WHERE u.email = %s AND u.senha_hash = %s
            """, (email, senha_hash))
            usuario = cursor.fetchone()
            return usuario  # retorna None se não achar
        except Error as e:
            print(f"Erro ao autenticar: {e}")
            return None
        finall
