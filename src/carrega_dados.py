import pandas as pd
import streamlit as st
from dados_online import buscar_dados_cotacoes_yahoo,buscar_dividendos_yahoo
from datetime import datetime, timedelta

CACHE_EXPIRATION_MINUTES = 30

def carregar_dados(ativos_config, use_cache=True):
    """
    Carrega os dados de cotações e dividendos, com opção de usar ou não o cache do Streamlit.
    O cache expira após um período definido.  Adiciona tela de loading.

    Args:
        ativos_config (dict): Configurações para buscar os ativos online.
        use_cache (bool, optional): Indica se deve usar o cache do Streamlit. Padrão é True.

    Returns:
        tuple: Um tuple contendo os DataFrames de cotações e dividendos.
                Retorna (None, None) em caso de falha total.
    """
    cache_key = f"dados_ativos_{ativos_config}"

    if use_cache and cache_key in st.session_state and 'data' in st.session_state[cache_key]:
        cached_data = st.session_state[cache_key]
        if datetime.now() < cached_data['expiry_time']:
            print("Carregando dados do cache...")
            return cached_data['data']
        else:
            print("Cache expirado, recarregando dados...")
            del st.session_state[cache_key]

    df_cotacoes_online = None
    df_dividendos_online = None

    # Adiciona o spinner para indicar o carregamento
    with st.spinner("Buscando dados online..."):
        try:
            print("Tentando carregar dados online...")
            # Carrega os dados online
            df_cotacoes_online = buscar_dados_cotacoes_yahoo(ativos_config)
            df_dividendos_online = buscar_dividendos_yahoo(ativos_config)
            print("Dados online carregados com sucesso!")
            dados = (df_cotacoes_online, df_dividendos_online)

            # Salva no cache
            expiry_time = datetime.now() + timedelta(minutes=CACHE_EXPIRATION_MINUTES)
            st.session_state[cache_key] = {'data': dados, 'expiry_time': expiry_time}
            return dados

        except Exception as e:
            print(f"Erro ao carregar dados online: {e}")
            print("Tentando carregar dados locais...")
            try:
                # Carrega os dados local
                df_cotacoes_local = pd.read_excel('data\dados_organizados.xlsx')
                df_dividendos_local = pd.read_excel('data\historico_dividendos.xlsx')
                print("Dados locais carregados com sucesso!")
                dados = (df_cotacoes_local, df_dividendos_local)
                expiry_time = datetime.now() + timedelta(minutes=CACHE_EXPIRATION_MINUTES)
                st.session_state[cache_key] = {'data': dados, 'expiry_time': expiry_time}
                return dados
            except Exception as e_local:
                print(f"Erro ao carregar dados locais: {e_local}")
                print("Falha ao carregar os dados online e locais.")
                return None, None