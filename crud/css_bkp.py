import streamlit as st

def local_css():
    st.markdown("""
        <style>
        /* ====== INPUTS ====== */
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stDateInput input {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 8px;
            font-size: 16px;
            transition: 0.3s;
        }

        /* Cor quando recebe foco */
        .stTextInput > div > div > input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {
            outline: none !important;
            border: 2px solid #FFD54F;  /* amarelo discreto */
            background-color: #FFF9C4;  /* fundo amarelo claro */
            color: #0D47A1;             /* fonte azul */
        }

        /* ====== BOTÕES - estilo base ====== */
        .stButton > button {
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
        }

        /* ====== BOTÕES ESPECÍFICOS ====== */
        /* Botões de Salvar (formulário principal e edição) */
        div.stButton > button[title^="Salvar"] {
            background-color: #2196F3 !important; /* azul */
        }
        div.stButton > button[title^="Salvar"]:hover {
            background-color: #1565C0 !important;
        }

        /* Botão Alterar */
        div.stButton > button[title^="Alterar"] {
            background-color: #007bff !important; /* azul */
        }
        div.stButton > button[title^="Alterar"]:hover {
            background-color: #0056b3 !important;
        }

        /* Botão Excluir */
        div.stButton > button[title^="Excluir"] {
            background-color: #F44336 !important; /* vermelho */
        }
        div.stButton > button[title^="Excluir"]:hover {
            background-color: #b71c1c !important;
        }

        /* Botão Cancelar */
        div.stButton > button[title^="Cancelar"] {
            background-color: #9E9E9E !important; /* cinza */
        }
        div.stButton > button[title^="Cancelar"]:hover {
            background-color: #616161 !important;
        }

        /* ====== EFEITOS GERAIS ====== */
        .stButton > button:hover {
            opacity: 0.95;
            transform: scale(1.05);
        }

        .stButton > button:active {
            transform: scale(0.97);
        }
        </style>
    """, unsafe_allow_html=True)
