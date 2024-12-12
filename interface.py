import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

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
    "RZTR11.SA": 90.21, "VGHF11.SA": 7.67, "GGRC11.SA": 10.49, "XPLG11.SA": 97.17,
    "XPML11.SA": 103.12, "VISC11.SA": 96,63, "GARE11.SA": 8.68, "HGRU11.SA": 113.68
}

# Configurações da interface
st.title("Análise de Ativos")
st.sidebar.header("Seleção de Ativo")

# Seleção do ativo e período de dias
ativo_selecionado = st.sidebar.selectbox("Escolha o ativo", ativos)
num_dias = st.sidebar.slider("Número de dias para exibir no gráfico", 1, 520, 15)

st.sidebar.header("Meses para exibir no gráfico")
meses = st.sidebar.slider("Dividendos dos últimos meses", 2, 12, 6)

# Exibe o gráfico para o ativo selecionado
grafico = gerar_grafico(ativo_selecionado, num_dias, precos_medios)
if grafico:
    st.plotly_chart(grafico, use_container_width=True)

grafico_dividendos = gerar_grafico_dividendos(ativo_selecionado,meses)
if grafico_dividendos:
    st.plotly_chart(grafico_dividendos, use_container_width=True)

# Calcula e exibe a tabela de dados dos ativos
st.write("Tabela de Dados dos Ativos", unsafe_allow_html=True)
df_ativos = calcular_dividendos_yields(ativos, precos_medios)

# Exibe a tabela com o ajuste de largura e altura do container
st.dataframe(df_ativos, use_container_width=True, height=458,hide_index=True)
# Estilo personalizado para ajustar o tamanho da fonte do cabeçalho e das linhas da tabela

