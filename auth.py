# auth.py
import streamlit as st
import hashlib
from db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def autenticar(email, senha):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DP_USUARIOS WHERE email=%s AND senha_hash=%s",
                   (email, hash_password(senha)))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def cadastrar_usuario(nome, email, senha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO DP_USUARIOS (nome, email, senha_hash, tipo_usuario) VALUES (%s,%s,%s,%s)",
                   (nome, email, hash_password(senha), "comum"))
    conn.commit()
    cursor.close()
    conn.close()

def recuperar_senha(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DP_USUARIOS WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return "Um link de redefinição de senha seria enviado por e-mail."
    return "E-mail não encontrado."
