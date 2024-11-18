import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

def gerar_grafico(ticker, num_dias, precos_medios):
    data = yf.download(ticker, period="max")
    data = data.tail(num_dias + 1)
    data['Variação %'] = data['Close'].pct_change() * 100

    if len(data) <= num_dias:
        return None
    data = data.tail(num_dias)
    current_day_data = data['Close'].iloc[-1]

    fig = go.Figure()
    if num_dias >= 16:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'], mode='lines+markers+text',
            name='Cotação', line=dict(color='blue')
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'], mode='lines+markers+text',
            name='Cotação', line=dict(color='blue'),
            text=[f"R$ {close:.2f}".replace('.', ',') + 
                f"<br>{'▲' if change > 0 else '▼'} {change:.2f}%".replace('.', ',')
                if not pd.isna(change) else f"R$ {close:.2f}".replace('.', ',')
                for close, change in zip(data['Close'], data['Variação %'])],
            textposition="top center",
            textfont=dict(size=13.5)
        ))


    preco_medio = precos_medios.get(ticker, None)
    if preco_medio is not None:
        fig.add_trace(go.Scatter(
            x=data.index, y=[preco_medio] * len(data), mode='lines',
            name="Preço Médio", line=dict(color='orange', dash='solid')
        ))

        fig.add_annotation(
            x=data.index[-1], y=preco_medio,
            text=f"Preço Médio: R$ {preco_medio:.2f}",
            showarrow=True, arrowhead=2, ax=0, ay=-40,
            bgcolor="orange", font=dict(color="white", size=13)
        )

        diferenca_percentual = ((current_day_data - preco_medio) / preco_medio) * 100
        fig.add_annotation(
            xref="paper", yref="paper", x=0.98,# y=0.3,
            text=f"Cotação atual vs. preço médio: {diferenca_percentual:.2f}%",
            showarrow=False, font=dict(size=13, color="white"),
            bgcolor="gray"
        )

    # Configuração do dtick com base no número de dias selecionados
    if num_dias > 30:
        dtick = "M1"  # Um marcador por mês
    elif num_dias > 10:
        dtick = "W1"  # Um marcador por semana
    else:
        dtick = "D1"  # Um marcador por dia

    fig.update_layout(
        title=f"Cotação do {ticker} nos últimos {num_dias} dias em comparação com preço médio",
        title_font=dict(size=20),
        yaxis_title="Cotação (R$)",
        yaxis=dict(
            title='Cotação (R$)',  # Título do eixo Y
            #title_font=dict(size=17),  # Aumenta o tamanho da fonte do título do eixo Y
            #tickfont=dict(size=17),  # Aumenta o tamanho da fonte dos ticks do eixo Y
        ),
        template="plotly_dark",
        xaxis=dict(
            tickformat="%d-%m-%Y",
            tickangle=-25,
            tickmode="linear",
            dtick=dtick
            #,tickfont=dict(size=15)

        )
    )

    return fig


def gerar_grafico_dividendos(ticker, meses):
    # Garante que o valor de meses esteja entre 2 e 12
    if meses < 2 or meses > 12:
        raise ValueError("O número de meses deve estar entre 2 e 12.")

    # Baixa os dados de dividendos e converte para ignorar o fuso horário
    data = yf.Ticker(ticker).dividends
    if data.empty:
        return None

    # Remove o fuso horário do índice
    data.index = data.index.tz_localize(None)

    # Filtra para os últimos 'meses' meses, definidos pelo parâmetro
    data = data[data.index >= (pd.Timestamp.now() - pd.DateOffset(months=meses))]

    # Converte para DataFrame e arredonda os valores
    data = data.to_frame(name='Dividendos')
    data['Dividendos'] = data['Dividendos'].round(2)
    data['Variação %'] = data['Dividendos'].pct_change().round(2) * 100

    # Cria o gráfico
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

    # Configurações do layout do gráfico
    fig.update_layout(
        title=f"Histórico de Dividendos do {ticker} - Últimos {meses} Meses",
        title_font=dict(size=20),
        yaxis_title="Dividendos (R$)",
        template="plotly_dark",
        xaxis=dict(
            tickformat="%Y-%m-%d",  # Formato de data sem horas
            tickangle=-25
        ),
        yaxis=dict(
            tickprefix="R$ "
        )
    )

    return fig


