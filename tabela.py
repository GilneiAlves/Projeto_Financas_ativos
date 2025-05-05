import pandas as pd
import numpy as np
import streamlit as st
from datetime import timedelta

def calcular_dividendos_yields(ativos, precos_medios, df_dividendos_excel, df_cotacoes_atual):
    """
    Calcula indicadores financeiros de dividendos e yields (DY e YOC) para uma lista de ativos.

    Parâmetros:
    - ativos: lista de tickers (ex: ['ITSA4', 'TAEE11'])
    - precos_medios: dicionário com preço médio de compra por ativo
    - df_dividendos_excel: DataFrame com histórico de dividendos pagos (colunas: 'ticker', 'date', 'dividendo')
    - df_cotacoes_atual: DataFrame com últimas cotações dos ativos (colunas: 'ticker', 'date', 'valor_cotação')

    Retorna:
    - DataFrame consolidado com métricas por ativo
    """

    dados_ativos = []  # Lista que armazenará os dados processados
    agora = pd.Timestamp.now()  # Data e hora atual para referência dos últimos 12 meses

    for ticker in ativos:
        try:
            # --- Carregar dividendos do ativo atual ---
            df_ticker_dividendos = df_dividendos_excel[df_dividendos_excel['ticker'] == ticker].copy()

            # Caso não existam dados de dividendos
            if df_ticker_dividendos.empty:
                st.warning(f"Não foram encontrados dividendos no arquivo para o ativo: {ticker}")
                preco_medio_raw = precos_medios.get(ticker, None)

                dados_ativos.append({
                    "Ativo": ticker,
                    "Preço Médio": f"R$ {preco_medio_raw:.2f}" if preco_medio_raw is not None else "-",
                    "Cotação Atual": "-",
                    "Dividendo 12 Mês": "-",
                    "Dividendo Mês atual": "-",
                    "Média dos Dividendos (12m)": "-",
                    "% Yield Atual (DY)": "-",
                    "% Yield on Cost (YOC)": "-"
                })
                continue  # Vai para o próximo ticker

            # --- Processar datas e filtrar dividendos dos últimos 12 meses ---
            df_ticker_dividendos['date'] = pd.to_datetime(df_ticker_dividendos['date'], format='%d/%m/%Y')
            data_limite = agora - pd.DateOffset(months=12)
            data_12_meses = df_ticker_dividendos[df_ticker_dividendos['date'] >= data_limite]

            # --- Cálculo dos dividendos e média ---
            dividendos_12m = round(data_12_meses['dividendo'].sum(), 2)
            media_dividendos = round(data_12_meses['dividendo'].mean(), 2) if not data_12_meses.empty else 0
            ultimo_dividendo = round(df_ticker_dividendos.iloc[-1]['dividendo'], 2)

            # Indicador de variação do último dividendo em relação à média
            if media_dividendos > 0:
                if ultimo_dividendo > media_dividendos:
                    variacao = "▲"
                elif ultimo_dividendo < media_dividendos:
                    variacao = "▼"
                else:
                    variacao = "-"
            else:
                variacao = ""

            # --- Cotação atual ---
            df_ticker_cotacoes = df_cotacoes_atual[df_cotacoes_atual['ticker'] == ticker].copy()
            if not df_ticker_cotacoes.empty:
                df_ticker_cotacoes['date'] = pd.to_datetime(df_ticker_cotacoes['date'])
                df_ticker_cotacoes_ordenado = df_ticker_cotacoes.sort_values(by='date', ascending=False)
                cotacao_atual = df_ticker_cotacoes_ordenado.iloc[0]['valor_cotação']
            else:
                cotacao_atual = np.nan
                st.warning(f"Não foram encontradas cotações para o ativo: {ticker}")

            # --- Preço médio e cálculos de yield ---
            preco_medio_raw = precos_medios.get(ticker, None)
            dy_atual = round((dividendos_12m / cotacao_atual) * 100, 2) if pd.notna(cotacao_atual) and cotacao_atual != 0 else np.nan
            yoc = round((dividendos_12m / preco_medio_raw) * 100, 2) if preco_medio_raw not in [None, 0] else np.nan

            # --- Consolidar dados no resultado final ---
            dados_ativos.append({
                "Ativo": ticker,
                "Preço Médio": f"R$ {preco_medio_raw:.2f}" if preco_medio_raw is not None else "-",
                "Cotação Atual": f"R$ {cotacao_atual:.2f}" if pd.notna(cotacao_atual) else "-",
                "Dividendo 12 Mês": f"R$ {dividendos_12m:.2f}",
                "Dividendo Mês atual": f"R$ {ultimo_dividendo:.2f}  ({variacao})",
                "Média dos Dividendos (12m)": f"R$ {media_dividendos:.2f}",
                "% Yield Atual (DY)": f"{dy_atual:.2f}%" if not np.isnan(dy_atual) else "-",
                "% Yield on Cost (YOC)": f"{yoc:.2f}%" if not np.isnan(yoc) else "-"
            })

        except Exception as e:
            # Em caso de erro durante o processamento de um ativo
            st.error(f"Erro ao processar o ativo {ticker}: {e}")
            preco_medio_raw = precos_medios.get(ticker, None)

            dados_ativos.append({
                "Ativo": ticker,
                "Preço Médio": f"R$ {preco_medio_raw:.2f}" if preco_medio_raw is not None else "-",
                "Cotação Atual": "-",
                "Dividendo 12 Mês": "-",
                "Dividendo Mês atual": "-",
                "Média dos Dividendos (12m)": "-",
                "% Yield Atual (DY)": "-",
                "% Yield on Cost (YOC)": "-"
            })

    # Converte lista final em DataFrame
    return pd.DataFrame(dados_ativos)
