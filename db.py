# db.py
import mysql.connector
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host="193.203.184.92",
        user="u576686179_start",
        password="IntNeg2025@!",
        database="u576686179_start"
    )
