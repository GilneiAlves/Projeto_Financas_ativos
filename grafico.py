# Importação de bibliotecas necessárias para coleta de dados, visualização e interface
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import timedelta
import yfinance as yf

# Gera gráfico de cotação
def gerar_grafico(ticker, num_dias, precos_medios):
    data = yf.download(ticker, period="max")
    data = data.xs(ticker, level="Ticker", axis=1)  # Necessário para yfinance>=0.2.54
    data = data.tail(num_dias + 1)
    data['Variação %'] = data['Close'].pct_change() * 100

    if len(data) <= num_dias:
        return None

    data = data.tail(num_dias)
    current_day_data = data['Close'].iloc[-1]

    fig = go.Figure()

    if num_dias >= 16:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines+markers+text',
            name='Cotação',
            line=dict(color='blue')
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines+markers+text',
            name='Cotação',
            line=dict(color='blue'),
            text=[
                f"R$ {close:.2f}".replace('.', ',') +
                f"<br>{'▲' if change > 0 else '▼'} {change:.2f}%".replace('.', ',')
                if not pd.isna(change) else f"R$ {close:.2f}".replace('.', ',')
                for close, change in zip(data['Close'], data['Variação %'])
            ],
            textposition="top center",
            textfont=dict(size=13.5)
        ))

    preco_medio = precos_medios.get(ticker, None)

    if preco_medio is not None:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=[preco_medio] * len(data),
            mode='lines',
            name="Preço Médio",
            line=dict(color='orange', dash='solid')
        ))

        fig.add_annotation(
            x=data.index[-1],
            y=preco_medio,
            text=f"Preço Médio: R$ {preco_medio:.2f}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            bgcolor="orange",
            font=dict(color="white", size=13)
        )

        diferenca_percentual = ((current_day_data - preco_medio) / preco_medio) * 100
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.98,
            text=f"Cotação atual vs. preço médio: {diferenca_percentual:.2f}%",
            showarrow=False,
            font=dict(size=13, color="white"),
            bgcolor="gray"
        )

    # Configuração do espaçamento de marcação no eixo X
    if num_dias > 30:
        dtick = "M1"  # Mensal
    elif num_dias > 10:
        dtick = "W1"  # Semanal
    else:
        dtick = "D1"  # Diário

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
        ),
        yaxis=dict(
            title='Cotação (R$)'
        )
    )

    return fig

# Gera gráfico de dividendos
def gerar_grafico_dividendos(ticker, meses):
    if meses < 2 or meses > 12:
        raise ValueError("O número de meses deve estar entre 2 e 12.")

    data = yf.Ticker(ticker).dividends
    if data.empty:
        return None

    data.index = data.index.tz_localize(None)
    data = data[data.index >= (pd.Timestamp.now() - pd.DateOffset(months=meses))]
    data = data.to_frame(name='Dividendos')
    data['Dividendos'] = data['Dividendos'].round(2)
    data['Variação %'] = data['Dividendos'].pct_change().round(2) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Dividendos'],
        mode='lines+markers+text',
        name='Dividendos',
        line=dict(color='blue'),
        text=[
            f"R$ {dividendo:.2f}".replace('.', ',') +
            (f"<br>{'▲' if variacao > 0 else '▼'} {variacao:.2f}%".replace('.', ',')
             if not pd.isna(variacao) else "")
            for dividendo, variacao in zip(data['Dividendos'], data['Variação %'])
        ],
        textposition="top center",
        textfont=dict(size=13.5)
    ))

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
