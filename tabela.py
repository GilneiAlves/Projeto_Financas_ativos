import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

# Função para calcular os dividendos e os yields
def calcular_dividendos_yields(ativos, precos_medios):
    dados_ativos = []

    for ticker in ativos:
        try:
            ativo = yf.Ticker(ticker)

            # Verifica se o histórico de preços existe
            historico = ativo.history(period="max")
            if historico.empty:
                st.write(f"Ticker: {ticker} não possui dados de cotação.")
                continue  # Passa para o próximo ativo se não houver dados

            cotacao_atual = round(historico['Close'][-1], 2)  # Último preço de fechamento arredondado para 2 casas
            
            preco_medio = precos_medios.get(ticker, None)
            preco_medio = round(preco_medio, 2) if preco_medio else None
            tipo_ativo = ativo.info.get("quoteType", "N/A") if ativo.info else "N/A"
            
            # Verificar se existem dividendos
            if ativo.dividends.empty:
                st.write(f"Ticker: {ticker} não possui dados de dividendos.")
                dividendos_12m = 0  # Se não houver dividendos, retorna 0
                media_dividendos = 0
                variacao = ""
            else:
                # Considera os dividendos dos últimos 12 meses
                dividendos_ultimos_12_meses = ativo.dividends[-12:]  # Dividendos dos últimos 12 meses
                dividendos_12m = round(dividendos_ultimos_12_meses.sum(), 2)  # Soma dos dividendos dos últimos 12 meses
                media_dividendos = round(dividendos_ultimos_12_meses.mean(), 2)  # Média dos dividendos dos últimos 12 meses
                
                # Calcular a variação entre o último dividendo e a média dos últimos 12 meses
                ultimo_dividendo = round(ativo.dividends[-1], 2)
                if media_dividendos > 0:
                    if ultimo_dividendo > media_dividendos:
                        variacao = "▲"  # Se o dividendo atual for maior que a média
                    elif ultimo_dividendo < media_dividendos:
                        variacao = "▼"  # Se o dividendo atual for menor que a média
                    else:
                        variacao = "-"  # Caso o dividendo atual seja igual à média
                else:
                    variacao = ""
            
            # Calcular o Dividend Yield Atual (DY) e Yield on Cost (YOC)
            dy_atual = round((dividendos_12m / cotacao_atual) * 100, 2) if cotacao_atual else np.nan
            yoc = round((dividendos_12m / preco_medio) * 100, 2) if preco_medio else np.nan

            # Adicionar dados ao dataframe
            dados_ativos.append({
                "Ativo": ticker,
                "Preço Médio": "R$ " + f"{preco_medio:.2f}".replace('.', ',') if preco_medio else "-",
                "Cotação Atual": "R$ " + f"{cotacao_atual:.2f}".replace('.', ','),
                "Dividendo 12 Mês": f"R$ {dividendos_12m:.2f}".replace('.', ','),
                "Dividendo Mês atual":   f"R$ {ultimo_dividendo:.2f}".replace('.', ',') + f"  ({variacao})",
                "Média dos Dividendos (12m)": f"R$ {media_dividendos:.2f}".replace('.', ','),
                "% Yield Atual (DY)": f"{dy_atual:.2f}".replace('.', ',') + "%",
                "% Yield on Cost (YOC)": f"{yoc:.2f}".replace('.', ',') + "%"
            })

        except Exception as e:
            st.write(f"Erro ao processar o ativo {ticker}: {e}")

    return pd.DataFrame(dados_ativos)
