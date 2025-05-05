import pandas as pd
import plotly.graph_objects as go

def gerar_grafico(ticker, num_dias, precos_medios, df_cotacoes):
    """
    Gera um gráfico de cotação para um determinado ticker, utilizando dados de um DataFrame
    carregado de um arquivo Excel.

    Args:
        ticker (str): O ticker do ativo para o qual gerar o gráfico.
        num_dias (int): O número de dias recentes a serem exibidos no gráfico.
        precos_medios (dict): Um dicionário contendo os preços médios dos ativos.
                              As chaves são os tickers e os valores são os preços médios.
        df_cotacoes (pd.DataFrame): DataFrame contendo as colunas 'date', 'ticker' e 'valor_cotação'.

    Returns:
        plotly.graph_objects.Figure: Um objeto Figure do Plotly contendo o gráfico de cotação,
                                      ou None se não houver dados suficientes para o ticker.
    """
    # Criamos um novo DataFrame contendo apenas as linhas correspondentes ao ticker desejado.
    df_ticker = df_cotacoes[df_cotacoes['ticker'] == ticker].copy()

    # Verifica se há dados para o ticker especificado após a filtragem.
    if df_ticker.empty:
        return None

    # Garante que as datas sejam tratadas corretamente para ordenação e filtragem.
    df_ticker['date'] = pd.to_datetime(df_ticker['date'], format='%d-%m-%Y')

    # Garante que os dados estejam na ordem cronológica correta para selecionar os últimos dias.
    df_ticker = df_ticker.sort_values(by='date')

    # Pegamos os últimos 'num_dias' registros para exibir no gráfico. Adicionamos 1 para calcular a variação.
    data = df_ticker.tail(num_dias + 1).set_index('date')

    # Adiciona uma coluna com a variação da cotação em relação ao dia anterior.
    data['Variação %'] = data['valor_cotação'].pct_change() * 100

    # Verifica se há dados suficientes para o número de dias solicitado.
    if len(data) <= num_dias:
        return None

    # Remove o primeiro dia usado apenas para calcular a variação.
    data = data.tail(num_dias)

    # Obtém o valor da cotação do último dia para exibir na anotação.
    current_day_data = data['valor_cotação'].iloc[-1]

    # Cria a figura do gráfico utilizando a biblioteca Plotly.
    fig = go.Figure()

    # Se o número de dias for maior ou igual a 16, exibe apenas linha e marcadores para evitar poluição visual.
    if num_dias >= 16:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['valor_cotação'], mode='lines+markers',
            name='Cotação', line=dict(color='blue')
        ))
    # Se o número de dias for menor que 16, exibe o valor e a variação em cada ponto.
    else:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['valor_cotação'], mode='lines+markers+text',
            name='Cotação', line=dict(color='blue'),
            text=[f"R$ {close:.2f}".replace('.', ',') +
                  f"<br>{'▲' if change > 0 else '▼'} {change:.2f}%".replace('.', ',')
                  if not pd.isna(change) else f"R$ {close:.2f}".replace('.', ',')
                  for close, change in zip(data['valor_cotação'], data['Variação %'])],
            textposition="top center",
            textfont=dict(size=13.5)
        ))

    # Adicionar a linha do preço médio ao gráfico, se disponível.
    preco_medio = precos_medios.get(ticker, None)
    if preco_medio is not None:
        fig.add_trace(go.Scatter(
            x=data.index, y=[preco_medio] * len(data), mode='lines',
            name="Preço Médio", line=dict(color='orange', dash='solid')
        ))

        # Adicionar uma anotação indicando o valor do preço médio.
        fig.add_annotation(
            x=data.index[-1], y=preco_medio,
            text=f"Preço Médio: R$ {preco_medio:.2f}".replace('.', ','),
            showarrow=True, arrowhead=2, ax=0, ay=-40,
            bgcolor="orange", font=dict(color="white", size=13)
        )

        # Calcular e adicionar anotação da diferença percentual entre a cotação atual e o preço médio.
        diferenca_percentual = ((current_day_data - preco_medio) / preco_medio) * 100
        fig.add_annotation(
            xref="paper", yref="paper", x=0.98,
            text=f"Cotação atual vs. preço médio: {diferenca_percentual:.2f}%".replace('.', ','),
            showarrow=False, font=dict(size=13, color="white"),
            bgcolor="gray"
        )

    # Ajusta o espaçamento dos ticks no eixo x com base no número de dias para melhor visualização.
    if num_dias > 30:
        dtick = "M1"  # Um marcador por mês
    elif num_dias > 10:
        dtick = "W1"  # Um marcador por semana
    else:
        dtick = "D1"  # Um marcador por dia

    # Configurar o layout do gráfico
    fig.update_layout(
        title=f"Cotação do {ticker} nos últimos {num_dias} dias em comparação com preço médio", # Define o título do gráfico, incluindo o ticker e o número de dias.
        title_font=dict(size=20), # Define o tamanho da fonte do título.
        yaxis_title="Cotação (R$)", # Define o título do eixo y (vertical), indicando a unidade da cotação.
        yaxis=dict(
            title='Cotação (R$)', # Redefine o título do eixo y dentro das configurações do eixo y.
        ),
        template="plotly_dark", # Define o tema visual do gráfico para um fundo escuro.
        xaxis=dict(
            tickformat="%d-%m-%Y", # Define o formato de exibição das datas nos ticks do eixo x (horizontal).
            tickangle=-25, # Rotaciona os rótulos do eixo x em -25 graus para evitar sobreposição.
            tickmode="linear", # Define o modo de exibição dos ticks como linear, espaçando-os uniformemente.
            dtick=dtick # Define o intervalo entre os ticks no eixo x, ajustado dinamicamente com base no número de dias.
        )
    )

    return fig

def gerar_grafico_dividendos(ticker, meses, df_dividendos):
    """
    Gera um gráfico de dividendos para um determinado ticker a partir de um DataFrame.

    Args:
        ticker (str): O ticker do ativo para o qual gerar o gráfico.
        meses (int): O número de meses recentes a serem exibidos no gráfico.
        df_dividendos (pd.DataFrame): DataFrame contendo as colunas 'ticker', 'date' e 'dividendo'.

    Returns:
        plotly.graph_objects.Figure: Um objeto Figure do Plotly contendo o gráfico de dividendos,
                                      ou None se não houver dados suficientes para o ticker.
    """

    # Criamos um novo DataFrame contendo apenas as linhas correspondentes ao ticker desejado.
    df_ticker_dividendos = df_dividendos[df_dividendos['ticker'] == ticker].copy()

    # Conversão da coluna de data para o tipo datetime.
    # Isso garante que as datas sejam tratadas corretamente para filtragem e ordenação.
    df_ticker_dividendos['date'] = pd.to_datetime(df_dividendos['date'], format='%d-%m-%Y')

    # Verifica se há dados para o ticker especificado após a filtragem.
    if df_ticker_dividendos.empty:
        return None

    # Mantemos apenas os dividendos que ocorreram nos últimos 'meses' meses.
    data_filtrada = df_ticker_dividendos[df_ticker_dividendos['date'] >= (pd.Timestamp.now() - pd.DateOffset(months=meses))]

    # Verifica se há dados dentro do período de tempo especificado.
    if data_filtrada.empty:
        return None

    # Ordenação dos dados por data. Isso garante que o gráfico exiba os dividendos em ordem cronológica.
    data_filtrada = data_filtrada.sort_values(by='date')

    # Cálculo da variação percentual dos dividendos. Isso adiciona uma coluna com a variação do dividendo em relação ao pagamento anterior.
    data_filtrada['Variação %'] = data_filtrada['dividendo'].pct_change().round(2) * 100

    # Cria a figura do gráfico utilizando a biblioteca Plotly.
    fig = go.Figure()

    # Adiciona um traço ao gráfico, que representa a linha dos dividendos ao longo do tempo.
    fig.add_trace(go.Scatter(
        x=data_filtrada['date'],
        y=data_filtrada['dividendo'],
        mode='lines+markers+text', # Exibe linhas, marcadores e texto nos pontos.
        name='Dividendos',
        line=dict(color='blue'),
        # Formatação do texto que aparece ao lado de cada ponto no gráfico.
        text=[
            f"R$ {dividendo:.2f}".replace('.', ',') +
            (f"<br>{'▲' if variacao > 0 else '▼'} {variacao:.2f}%".replace('.', ',')
             if not pd.isna(variacao) else "") # Adiciona a variação se disponível.
            for dividendo, variacao in zip(data_filtrada['dividendo'], data_filtrada['Variação %'])
        ],
        textposition="top center", # Posiciona o texto acima do ponto.
        textfont=dict(size=13.5)
    ))

    # Configuração do layout do gráfico
    fig.update_layout(
        title=f"Histórico de Dividendos do {ticker} - Últimos {meses} Meses",
        title_font=dict(size=20),
        yaxis_title="Dividendos (R$)",
        template="plotly_dark", # Define o tema escuro para o gráfico.
        xaxis=dict(
            tickformat='%d-%m-%Y', # Formato de exibição das datas no eixo x.
            tickangle=-25 # Rotaciona os rótulos do eixo x para evitar sobreposição.
        ),
        yaxis=dict(
            tickprefix="R$ " # Adiciona o prefixo "R$" aos valores do eixo y.
        )
    )

    return fig