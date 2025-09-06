import hashlib
from db import get_connection  # importa a função centralizada de conexão


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
        try:
            with conn.cursor() as cursor:
                senha_hash = hash_senha(senha)
                cursor.execute("""
                    SELECT u.id, u.nome, u.email, u.tipo_usuario, u.empresa_id, e.razao_social
                    FROM DP_USUARIOS u
                    LEFT JOIN EMPRESA e ON u.empresa_id = e.CODIGO
                    WHERE u.email = %s AND u.senha_hash = %s
                """, (email, senha_hash))
                usuario = cursor.fetchone()
                return usuario  # retorna None se não achar
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return None
        finally:
            conn.close()
    return None
