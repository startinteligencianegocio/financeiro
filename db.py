import pymysql
from pymysql.err import MySQLError


def get_connection():
    try:
        conn = pymysql.connect(
            host="193.203.184.92",
            user="u576686179_start",
            password="IntNeg2025@!",
            database="u576686179_start",
            cursorclass=pymysql.cursors.DictCursor,  # retorna resultados como dicionários
            charset="utf8mb4",
            autocommit=True  # evita problemas de commits esquecidos
        )
        return conn
    except MySQLError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
