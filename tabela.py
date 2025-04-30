import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
from datetime import timedelta

# Dicionários para cache local das informações, evitando múltiplas chamadas à API do yfinance
CACHE_INFO = {}
CACHE_HISTORICO = {}
CACHE_DIVIDENDOS_ATIVOS = {}
CACHE_VALIDADE = timedelta(minutes=30)  # Validade do cache (30 minutos)

# --- Funções internas para download de dados com tratamento de erros ---

def _download_info(ticker):
    """
    Baixa informações gerais do ativo (nome, tipo, etc).
    Retorna None em caso de falha na requisição.
    """
    try:
        ativo = yf.Ticker(ticker)
        return ativo.info
    except Exception as e:
        print(f"Erro ao baixar info para {ticker}: {e}")
        return None

def _download_historico(ticker, period="max"):
    """
    Baixa histórico de preços do ativo.
    Retorna None se ocorrer falha ou se os dados estiverem vazios.
    """
    try:
        ativo = yf.Ticker(ticker)
        historico = ativo.history(period=period)
        return historico
    except Exception as e:
        print(f"Erro ao baixar histórico para {ticker}: {e}")
        return None

def _download_dividendos_ativo(ticker):
    """
    Baixa os dividendos históricos do ativo.
    Retorna None se ocorrer falha ou os dados estiverem vazios.
    """
    try:
        ativo = yf.Ticker(ticker)
        return ativo.dividends
    except Exception as e:
        print(f"Erro ao baixar dividendos para {ticker}: {e}")
        return None

# --- Função principal ---

def calcular_dividendos_yields(ativos, precos_medios):
    """
    Calcula dividendos dos últimos 12 meses, dividend yield atual (DY)
    e yield on cost (YOC) para uma lista de ativos.

    Parâmetros:
    - ativos: lista de tickers (ex: ['PETR4.SA'])
    - precos_medios: dicionário com preços médios de compra por ticker

    Retorno:
    - DataFrame com informações financeiras por ativo
    """
    dados_ativos = []
    agora = pd.Timestamp.now()

    for ticker in ativos:
        try:
            # --- Informações Gerais ---
            if ticker in CACHE_INFO and agora - CACHE_INFO[ticker]['timestamp'] < CACHE_VALIDADE:
                info = CACHE_INFO[ticker]['data']
                print(f"Usando info em cache para {ticker}")
            else:
                print(f"Baixando info para {ticker}")
                info = _download_info(ticker)
                if info:
                    CACHE_INFO[ticker] = {'data': info, 'timestamp': agora}
                else:
                    info = {}  # Garante estrutura vazia em caso de erro

            # --- Histórico de Preços ---
            if ticker in CACHE_HISTORICO and agora - CACHE_HISTORICO[ticker]['timestamp'] < CACHE_VALIDADE:
                historico = CACHE_HISTORICO[ticker]['data'].copy()
                print(f"Usando histórico em cache para {ticker}")
            else:
                print(f"Baixando histórico para {ticker}")
                historico = _download_historico(ticker)
                if historico is not None and not historico.empty:
                    CACHE_HISTORICO[ticker] = {'data': historico.copy(), 'timestamp': agora}
                else:
                    st.write(f"Ticker: {ticker} não possui dados de cotação.")
                    continue

            cotacao_atual = round(historico['Close'][-1], 2)
            preco_medio = round(precos_medios.get(ticker, None), 2) if precos_medios.get(ticker) is not None else None
            tipo_ativo = info.get("quoteType", "N/A")  # Tipo de ativo (ação, ETF, etc.)

            # --- Dividendos ---
            if ticker in CACHE_DIVIDENDOS_ATIVOS and agora - CACHE_DIVIDENDOS_ATIVOS[ticker]['timestamp'] < CACHE_VALIDADE:
                dividendos = CACHE_DIVIDENDOS_ATIVOS[ticker]['data'].copy()
                print(f"Usando dividendos em cache para {ticker}")
            else:
                print(f"Baixando dividendos para {ticker}")
                dividendos_serie = _download_dividendos_ativo(ticker)
                if dividendos_serie is not None and not dividendos_serie.empty:
                    dividendos = dividendos_serie.copy()
                    dividendos.index = dividendos.index.tz_convert(None)  # Remove fuso horário
                    CACHE_DIVIDENDOS_ATIVOS[ticker] = {'data': dividendos.copy(), 'timestamp': agora}
                else:
                    dividendos = pd.Series()  # Cria série vazia

            # --- Cálculo dos Dividendos e Yields ---
            if not dividendos.empty:
                dividendos_ultimos_12_meses = dividendos[dividendos.index >= (agora - pd.DateOffset(months=12))]
                dividendos_12m = round(dividendos_ultimos_12_meses.sum(), 2)
                media_dividendos = round(dividendos_ultimos_12_meses.mean(), 2)
                ultimo_dividendo = round(dividendos[-1], 2)

                # Seta tendência do último dividendo em relação à média
                if media_dividendos > 0:
                    if ultimo_dividendo > media_dividendos:
                        variacao = "▲"
                    elif ultimo_dividendo < media_dividendos:
                        variacao = "▼"
                    else:
                        variacao = "-"
                else:
                    variacao = ""
            else:
                # Default caso não existam dividendos registrados
                dividendos_12m = 0
                media_dividendos = 0
                ultimo_dividendo = 0
                variacao = ""

            # Calcula os indicadores de yield
            dy_atual = round((dividendos_12m / cotacao_atual) * 100, 2) if cotacao_atual else np.nan
            yoc = round((dividendos_12m / preco_medio) * 100, 2) if preco_medio else np.nan

            # --- Adiciona dados à lista final ---
            dados_ativos.append({
                "Ativo": ticker,
                "Preço Médio": "R$ " + f"{preco_medio:.2f}".replace('.', ',') if preco_medio is not None else "-",
                "Cotação Atual": "R$ " + f"{cotacao_atual:.2f}".replace('.', ','),
                "Dividendo 12 Mês": f"R$ {dividendos_12m:.2f}".replace('.', ','),
                "Dividendo Mês atual": f"R$ {ultimo_dividendo:.2f}".replace('.', ',') + f"  ({variacao})",
                "Média dos Dividendos (12m)": f"R$ {media_dividendos:.2f}".replace('.', ','),
                "% Yield Atual (DY)": f"{dy_atual:.2f}".replace('.', ',') + "%" if not np.isnan(dy_atual) else "-",
                "% Yield on Cost (YOC)": f"{yoc:.2f}".replace('.', ',') + "%" if not np.isnan(yoc) else "-"
            })

        except Exception as e:
            # Trata qualquer erro inesperado por ativo
            st.write(f"Erro ao processar o ativo {ticker}: {e}")

    # Constrói DataFrame final
    return pd.DataFrame(dados_ativos)
