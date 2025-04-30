# Importação de bibliotecas necessárias para coleta de dados, visualização e interface
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import timedelta

# Dicionários utilizados para armazenar dados em cache, evitando requisições desnecessárias
CACHE_COTACOES = {}
CACHE_DIVIDENDOS = {}
CACHE_VALIDADE = timedelta(minutes=30)  # Tempo de validade do cache (30 minutos)

def _download_data(ticker, period="max"):
    """Função interna para baixar os dados históricos do ativo usando yfinance.
    Implementa tratamento de erros e suporte à nova estrutura do yfinance (>= 0.2.54)."""
    try:
        data = yf.download(ticker, period=period)
        if data is not None and not data.empty:
            return data.xs(ticker, level="Ticker", axis=1)  # Necessário para múltiplos tickers
        return None
    except Exception as e:
        print(f"Erro ao baixar dados para {ticker}: {e}")
        return None

def gerar_grafico(ticker, num_dias, precos_medios):
    """Gera gráfico de cotação dos últimos 'num_dias' dias, comparando com preço médio.
    Utiliza cache para evitar downloads redundantes."""
    agora = pd.Timestamp.now()

    # Verifica se dados estão em cache e ainda válidos
    if ticker in CACHE_COTACOES and agora - CACHE_COTACOES[ticker]['timestamp'] < CACHE_VALIDADE:
        data = CACHE_COTACOES[ticker]['data'].copy()
        print(f"Usando dados de cotação em cache para {ticker}")
    else:
        print(f"Baixando dados de cotação para {ticker}")
        data = _download_data(ticker, period="max")
        if data is not None:
            CACHE_COTACOES[ticker] = {'data': data.copy(), 'timestamp': agora}
        else:
            return None

    # Verifica se há dados suficientes
    if data is None or len(data) <= num_dias:
        return None

    # Seleciona apenas os últimos 'num_dias' de dados e calcula variação percentual
    data = data.tail(num_dias + 1).copy()
    data['Variação %'] = data['Close'].pct_change() * 100
    data = data.tail(num_dias)
    current_day_data = data['Close'].iloc[-1]

    fig = go.Figure()

    # Exibe labels de texto apenas para períodos curtos, para evitar poluição visual
    if num_dias >= 16:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'], mode='lines+markers+text',
            name='Cotação', line=dict(color='blue')
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'], mode='lines+markers+text',
            name='Cotação', line=dict(color='blue'),
            text=[
                f"R$ {close:.2f}".replace('.', ',') +
                f"<br>{'▲' if change > 0 else '▼'} {change:.2f}%".replace('.', ',')
                if not pd.isna(change) else f"R$ {close:.2f}".replace('.', ',')
                for close, change in zip(data['Close'], data['Variação %'])
            ],
            textposition="top center",
            textfont=dict(size=13.5)
        ))

    # Adiciona linha do preço médio, se disponível
    preco_medio = precos_medios.get(ticker, None)
    if preco_medio is not None and not pd.isna(preco_medio):
        fig.add_trace(go.Scatter(
            x=data.index, y=[preco_medio] * len(data), mode='lines',
            name="Preço Médio", line=dict(color='orange', dash='solid')
        ))

        # Anotação visual do preço médio no gráfico
        fig.add_annotation(
            x=data.index[-1], y=preco_medio,
            text=f"Preço Médio: R$ {preco_medio:.2f}",
            showarrow=True, arrowhead=2, ax=0, ay=-40,
            bgcolor="orange", font=dict(color="white", size=13)
        )

        # Exibe variação percentual da cotação atual em relação ao preço médio
        diferenca_percentual = ((current_day_data - preco_medio) / preco_medio) * 100
        fig.add_annotation(
            xref="paper", yref="paper", x=0.98,
            text=f"Cotação atual vs. preço médio: {diferenca_percentual:.2f}%",
            showarrow=False, font=dict(size=13, color="white"),
            bgcolor="gray"
        )

    # Ajusta intervalo de marcação no eixo X de acordo com o período analisado
    if num_dias > 30:
        dtick = "M1"  # Exibe um marcador por mês
    elif num_dias > 10:
        dtick = "W1"  # Exibe um marcador por semana
    else:
        dtick = "D1"  # Exibe um marcador por dia

    # Configuração estética do layout do gráfico
    fig.update_layout(
        title=f"Cotação do {ticker} nos últimos {num_dias} dias em comparação com preço médio",
        title_font=dict(size=20),
        yaxis_title="Cotação (R$)",
        template="plotly_dark",
        xaxis=dict(
            tickformat="%d-%m-%Y",
            tickangle=-25,
            tickmode="linear",
            dtick=dtick
        )
    )

    return fig

def gerar_grafico_dividendos(ticker, meses):
    """Gera gráfico de dividendos pagos nos últimos 'meses' meses para o ticker informado.
    Utiliza cache para otimizar a performance."""
    agora = pd.Timestamp.now()
    cache_key = f"{ticker}_{meses}"

    # Verifica se dados de dividendos estão em cache
    if cache_key in CACHE_DIVIDENDOS and agora - CACHE_DIVIDENDOS[cache_key]['timestamp'] < CACHE_VALIDADE:
        data = CACHE_DIVIDENDOS[cache_key]['data'].copy()
        print(f"Usando dados de dividendos em cache para {ticker} ({meses} meses)")
        if data.empty:
            st.warning(f"Não há dados de dividendos em cache para {ticker} nos últimos {meses} meses.")
            return None
    else:
        print(f"Baixando dados de dividendos para {ticker} ({meses} meses)")
        try:
            ativo = yf.Ticker(ticker)
            data_yf = ativo.dividends
            if not data_yf.empty:
                data_yf.index = data_yf.index.tz_localize(None)  # Remove timezone para evitar conflitos
                data = data_yf[data_yf.index >= (pd.Timestamp.now() - pd.DateOffset(months=meses))].copy()
                data = data.to_frame(name='Dividendos')
                CACHE_DIVIDENDOS[cache_key] = {'data': data.copy(), 'timestamp': agora}
                if data.empty:
                    st.warning(f"Não foram encontrados dados de dividendos para {ticker} nos últimos {meses} meses.")
                    return None
            else:
                st.warning(f"Não foram encontrados dados de dividendos para o ticker {ticker}.")
                return None
        except yf.exceptions.YFError as e:
            st.error(f"Erro ao buscar dados de dividendos para {ticker} (Yahoo Finance Error): {e}")
            return None
        except Exception as e:
            st.error(f"Erro inesperado ao buscar dados de dividendos para {ticker}: {e}")
            return None

    if data is None or data.empty:
        return None

    try:
        # Arredondamento dos valores e cálculo da variação percentual
        data['Dividendos'] = data['Dividendos'].round(2)
        data['Variação %'] = data['Dividendos'].pct_change().round(2) * 100
    except Exception as e:
        st.error(f"Erro ao processar dados de dividendos para {ticker}: {e}")
        return None

    # Criação do gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Dividendos'], mode='lines+markers+text',
        name='Dividendos', line=dict(color='blue'),
        text=[
            f"R$ {dividendo:.2f}".replace('.', ',') +
            (f"<br>{'▲' if variacao > 0 else '▼'} {variacao:.2f}%".replace('.', ',')
             if not pd.isna(variacao) else "")
            for dividendo, variacao in zip(data['Dividendos'], data['Variação %'])
        ],
        textposition="top center",
        textfont=dict(size=13.5)
    ))

    # Layout com estética escura e configurações de eixos
    fig.update_layout(
        title=f"Histórico de Dividendos do {ticker} - Últimos {meses} Meses",
        title_font=dict(size=20),
        yaxis_title="Dividendos (R$)",
        template="plotly_dark",
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickangle=-25
        ),
        yaxis=dict(
            tickprefix="R$ "
        )
    )

    return fig
