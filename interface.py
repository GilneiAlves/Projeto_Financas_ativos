import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz
import locale

from grafico import gerar_grafico
from tabela import calcular_dividendos_yields
from grafico import gerar_grafico_dividendos

# Configurações de página do Streamlit (wide mode)
st.set_page_config(
    page_title="Análise de Ativos",
    page_icon="📈",
    layout="wide",  # usar o layout "wide"
    initial_sidebar_state="expanded"
)

# Lista de ativos e preços médios
ativos = ["HGRU11.SA", "HSLG11.SA", "KNCR11.SA", "MXRF11.SA", "PORD11.SA", "RZTR11.SA", 
          "VGHF11.SA", "GGRC11.SA", "XPLG11.SA", "XPML11.SA", "GARE11.SA", "VISC11.SA"]

precos_medios = {
    "KNCR11.SA": 104.4, "HSLG11.SA": 84.99, "MXRF11.SA": 9.84, "PORD11.SA": 8.51,
    "RZTR11.SA": 90.21, "VGHF11.SA": 7.67, "GGRC11.SA": 10.31, "XPLG11.SA": 97.17,
    "XPML11.SA": 101.36, "VISC11.SA": 96.63, "GARE11.SA": 8.66, "HGRU11.SA": 113.68
}

# Configurações da interface
st.title("Análise de Ativos")
st.sidebar.header("Seleção de Ativo")

# Seleção do ativo e período de dias
ativo_selecionado = st.sidebar.selectbox("Escolha o ativo", ativos)
num_dias = st.sidebar.slider("Número de dias para exibir no gráfico", 1, 520, 15)

st.sidebar.header("Meses para exibir no gráfico")
meses = st.sidebar.slider("Dividendos dos últimos meses", 2, 12, 12)

# Entrada dos valores pelo usuário
st.sidebar.header("Parâmetros de Cálculo de Variação")
saldo_bruto = st.sidebar.number_input("Saldo Bruto", min_value=0.0, value=20000.0, step=100.0,format="%.2f")
valor_aplicado = st.sidebar.number_input("Valor Aplicado", min_value=0.0, value=30000.0, step=100.0,format="%.2f")
total_proventos = st.sidebar.number_input("Total de Proventos", min_value=0.0, value=700.0, step=10.0,format="%.2f")

# Cálculo da variação Real
variacao = (saldo_bruto - (valor_aplicado - total_proventos)) / saldo_bruto * 100

# Cálculo da variação de cotas
variacao_cotas = ((saldo_bruto - valor_aplicado) / valor_aplicado) * 100

# Exibição dos cards lado a lado
col1, col2 = st.columns(2)  # Criação de duas colunas

with col1:
    st.metric(label="Variação (%)", value=f"{variacao:.2f}%")

with col2:
    st.metric(label="Variação Cotas (%)", value=f"{variacao_cotas:.2f}%")

# Exibe o gráfico para o ativo selecionado
grafico = gerar_grafico(ativo_selecionado, num_dias, precos_medios)
if grafico:
    st.plotly_chart(grafico, use_container_width=True)

grafico_dividendos = gerar_grafico_dividendos(ativo_selecionado, meses)
if grafico_dividendos:
    st.plotly_chart(grafico_dividendos, use_container_width=True)

# Calcula e exibe a tabela de dados dos ativos
st.write("Tabela de Dados dos Ativos", unsafe_allow_html=True)
df_ativos = calcular_dividendos_yields(ativos, precos_medios)

# Exibe a tabela com o ajuste de largura e altura do container
st.dataframe(df_ativos, use_container_width=True, height=458, hide_index=True)