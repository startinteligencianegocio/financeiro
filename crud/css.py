import streamlit as st

def local_css():
    st.markdown("""
        <style>
        /* ===== BOTÃO SALVAR DO FORMULÁRIO ===== */
        div.stButton > button:first-child {
            background-color: #28a745;  /* verde */
            color: white;
            height: 35px;
            border-radius: 5px;
            font-weight: bold;
        }

        /* ===== BOTÃO ALTERAR ===== */
        div.stButton > button[key^="alt_forma_"] {
            background-color: #1E90FF;  /* azul */
            color: white;
            height: 30px;
            border-radius: 5px;
            font-weight: bold;
        }

        /* ===== BOTÃO EXCLUIR ===== */
        div.stButton > button[key^="del_forma_"] {
            background-color: #FF4C4C;  /* vermelho */
            color: white;
            height: 30px;
            border-radius: 5px;
            font-weight: bold;
        }
                
        .card {
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 8px #ccc;
            background-color: #f9f9f9;
        }                
        </style>
    """, unsafe_allow_html=True)
