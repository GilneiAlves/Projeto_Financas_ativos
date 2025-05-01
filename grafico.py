import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from yfinance.exceptions import YFRateLimitError

# Gera gráfico cotação
def gerar_grafico(ticker, num_dias, precos_medios):
    try:
        # Ajusta o período de download para o mínimo necessário
        dias_extra = 5
        total_dias = num_dias + dias_extra
        data = yf.download(ticker, period=f"{total_dias}d", progress=False)

        # Trata caso venha multiindex
        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs(ticker, level="Ticker", axis=1)

        data = data.tail(num_dias + 1)
        if data.empty or len(data) <= num_dias:
            return None

        data['Variação %'] = data['Close'].pct_change() * 100
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
                      (f"<br>{'▲' if change > 0 else '▼'} {change:.2f}%".replace('.', ',')
                       if not pd.isna(change) else "")
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
                xref="paper", yref="paper", x=0.98,
                text=f"Cotação atual vs. preço médio: {diferenca_percentual:.2f}%",
                showarrow=False, font=dict(size=13, color="white"),
                bgcolor="gray"
            )

        # Ajuste do espaçamento de datas no eixo X
        dtick = "D1" if num_dias <= 10 else "W1" if num_dias <= 30 else "M1"

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

    except YFRateLimitError:
        print("Limite de requisições atingido.")
        return None
    except Exception as e:
        print(f"Erro ao gerar gráfico de cotação: {e}")
        return None

# Gera gráfico de dividendos
def gerar_grafico_dividendos(ticker, meses):
    try:
        if meses < 2 or meses > 12:
            raise ValueError("O número de meses deve estar entre 2 e 12.")

        # Usa cache se estiver usando Streamlit (descomente se quiser)
        # @st.cache_data(ttl=3600)
        data = yf.Ticker(ticker).dividends

        if data.empty:
            return None

        data.index = data.index.tz_localize(None)
        data = data[data.index >= (pd.Timestamp.now() - pd.DateOffset(months=meses))]

        if data.empty:
            return None

        data = data.to_frame(name='Dividendos')
        data['Dividendos'] = data['Dividendos'].round(2)
        data['Variação %'] = data['Dividendos'].pct_change().round(2) * 100

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

    except YFRateLimitError:
        print("Limite de requisições atingido.")
        return None
    except Exception as e:
        print(f"Erro ao gerar gráfico de dividendos: {e}")
        return None
