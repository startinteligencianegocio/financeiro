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

        /* ====== BOTÕES ====== */
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
        .st.form_submit_button > button {
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
        } 
                
        /* Botões customizados por posição */
        div.stButton > button:first-child { background-color: #4CAF50; }  /* verde - Incluir */
        div.stButton > button:nth-child(2) { background-color: #FFD600; color: black; } /* amarelo - Alterar */
        div.stButton > button:nth-child(3) { background-color: #F44336; }  /* vermelho - Excluir */
        div.stButton > button:nth-child(4) { background-color: #2196F3; }  /* azul - Gravar */
        div.stButton > button:nth-child(5) { background-color: #9E9E9E; }  /* cinza - Cancelar */

        /* Efeitos hover */
        .stButton > button:hover {
            opacity: 0.9;
            transform: scale(1.05);
        }

        /* Efeito clique */
        .stButton > button:active {
            transform: scale(0.97);
        }
        </style>
    """, unsafe_allow_html=True)
