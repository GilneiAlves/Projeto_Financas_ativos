import requests
import pandas as pd
import time
from datetime import datetime, timedelta

def buscar_dados_cotacoes_yahoo(tickers: list,
                                 days_range=520,
                                 interval: str = '1d',
                                 sleep_seconds: float = 1.5,
                                 user_agent: str = 'Mozilla/5.0') -> pd.DataFrame:
    """
    Busca preços de fechamento (close) de múltiplos ativos no Yahoo Finance,
    dos últimos 520 dias até hoje.

    Retorna DataFrame com colunas: date | ticker | valor_cotação
    """
    all_data = []

    # Define intervalo de datas
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_range)

    period1 = int(start_date.timestamp())
    period2 = int(end_date.timestamp())

    for ticker in tickers:
        print(f" Baixando dados de: {ticker}")

        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            'period1': period1,
            'period2': period2,
            'interval': interval,
            'events': 'history'
        }
        headers = {
            'User-Agent': user_agent
        }

        try:
            time.sleep(sleep_seconds)
            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(f" Falha ao buscar {ticker}: HTTP {response.status_code}")
                continue

            data = response.json()
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            closes = result['indicators']['quote'][0]['close']

            df = pd.DataFrame({
                'date': [datetime.fromtimestamp(ts).strftime('%d/%m/%Y')for ts in timestamps],
                'valor_cotação': closes
            })
            df['ticker'] = ticker
            all_data.append(df)

        except Exception as e:
            print(f" Erro ao processar {ticker}: {e}")
            continue

    if all_data:
        df_final = pd.concat(all_data, ignore_index=True)
        df_final['valor_cotação'] = df_final['valor_cotação'].round(2)
        return df_final[['date', 'ticker', 'valor_cotação']].dropna()
    else:
        print("Nenhum dado válido retornado.")
        return pd.DataFrame(columns=['date', 'ticker', 'valor_cotação'])


def buscar_dividendos_yahoo(tickers: list,
                              days_range=365,
                              sleep_seconds: float = 1.5,
                              user_agent: str = 'Mozilla/5.0') -> pd.DataFrame:
    """
    Busca os dividendos pagos nos últimos 12 meses para múltiplos ativos via Yahoo Finance.
    
    Retorna DataFrame com colunas: date | ticker | valor_dividendo
    """
    all_data = []

    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_range)

    period1 = int(start_date.timestamp())
    period2 = int(end_date.timestamp())

    for ticker in tickers:
        print(f"Buscando dividendos: {ticker}")

        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            'period1': period1,
            'period2': period2,
            'interval': '1d',
            'events': 'div'  # <-- Importante: pega eventos de dividendos
        }
        headers = {
            'User-Agent': user_agent
        }

        try:
            time.sleep(sleep_seconds)
            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(f"Falha ao buscar dividendos de {ticker}: HTTP {response.status_code}")
                continue

            data = response.json()
            result = data['chart']['result'][0]

            if 'events' not in result or 'dividends' not in result['events']:
                print(f"Nenhum dividendo encontrado para {ticker}")
                continue

            dividends = result['events']['dividends']
            df = pd.DataFrame.from_dict(dividends, orient='index')

            df['date'] = pd.to_datetime(df['date'], unit='s').dt.strftime('%d/%m/%Y')
            df['ticker'] = ticker
            df.rename(columns={'amount': 'dividendo'}, inplace=True)
            all_data.append(df[['date', 'ticker', 'dividendo']])

        except Exception as e:
            print(f" Erro ao processar {ticker}: {e}")
            continue

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("Nenhum dividendo válido retornado.")
        return pd.DataFrame(columns=['date', 'ticker', 'dividendo'])
