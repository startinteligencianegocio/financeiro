# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection
from datetime import datetime, date
import css
import locale

# Configurar locale para pt_BR
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def input_data(label, valor_padrao):
    """
    Input de data no formato DD/MM/YYYY.
    Retorna um objeto datetime.date ou None se inválido.
    """
    data_str = st.text_input(label, valor_padrao.strftime("%d/%m/%Y"))
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        st.error("Data inválida! Use o formato DD/MM/YYYY")
        return None
    return data_obj

def show():
    # Aplicar CSS personalizado
    css.local_css()
    
    st.title("📊 Dashboard Financeiro")

    # === Inputs de data ===
    col1, col2 = st.columns(2)
    with col1:
        # Primeiro dia do mês corrente
        primeiro_dia_mes = date(datetime.now().year, datetime.now().month, 1)
        data_inicial = input_data("📅 Data inicial", primeiro_dia_mes)
    with col2:
        data_final = input_data("📅 Data final", datetime.now())

    # Validar se datas são válidas antes de consultar
    if data_inicial is None or data_final is None:
        st.stop()  # Interrompe execução até datas corretas

    # Converter para formato YYYY-MM-DD para SQL
    data_inicial_db = data_inicial.strftime("%Y-%m-%d")
    data_final_db = data_final.strftime("%Y-%m-%d")

    # === Conexão com banco de dados ===
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # === Consulta SQL com filtro de datas ===
    cursor.execute("""
        SELECT tipo_receita_despesas, SUM(valor) as total
        FROM DP_MOVIMENTACOES
        WHERE data_vencimento BETWEEN %s AND %s
        GROUP BY tipo_receita_despesas
    """, (data_inicial_db, data_final_db))
    
    dados = cursor.fetchall()
    cursor.close()
    conn.close()

    # === Criar DataFrame ===
    df = pd.DataFrame(dados)

    receitas = df[df["tipo_receita_despesas"]=="R"]["total"].sum() if not df.empty else 0
    despesas = df[df["tipo_receita_despesas"]=="D"]["total"].sum() if not df.empty else 0
    saldo = receitas - despesas

    # === KPIs coloridos com HTML/CSS ===
    col1, col2, col3 = st.columns(3)

    # Receita (verde)
    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: green;
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            ">
                <h4>Receitas</h4>
                <h3>R$ {receitas:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Despesas (vermelho)
    with col2:
        st.markdown(
            f"""
            <div style="
                background-color: red;
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            ">
                <h4>Despesas</h4>
                <h3>R$ {despesas:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Saldo (dinâmico: verde positivo, vermelho negativo, azul neutro)
    saldo_cor = "green" if saldo > 0 else "red" if saldo < 0 else "blue"
    with col3:
        st.markdown(
            f"""
            <div style="
                background-color: {saldo_cor};
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            ">
                <h4>Saldo</h4>
                <h3>R$ {saldo:,.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    # === Gráfico de barras ===
    if not df.empty:
        fig = px.bar(
            df,
            x="tipo_receita_despesas",
            y="total",
            color="tipo_receita_despesas",
            labels={"tipo_receita_despesas": "Tipo", "total": "Valor"},
            color_discrete_map={
                "R": "green",   # Receitas em verde
                "D": "red"      # Despesas em vermelho
            },
            text_auto='.2s',   # mostra valores nas barras
            height=350,        # altura do gráfico em pixels
            width=800          # largura do gráfico em pixels
        )

        # Layout com borda dentro do próprio gráfico
        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor="white",
            paper_bgcolor="white",
            bargap=0.4,
            margin=dict(l=40, r=40, t=40, b=40),
            shapes=[
                dict(
                    type="rect",
                    xref="paper", yref="paper",
                    x0=0, y0=0, x1=1, y1=1,
                    line=dict(color=saldo_cor, width=3),
                    layer="below"
                )
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ Nenhum dado encontrado para o período selecionado.")
