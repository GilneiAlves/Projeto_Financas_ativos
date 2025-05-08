# Análise de Ativos com Streamlit e yFinance
# https://gilneialvesfinancas.streamlit.app/

Este projeto realiza a análise de ativos financeiros utilizando a biblioteca `yfinance` para buscar dados históricos de ações e o `Streamlit` para criar uma interface interativa que permite visualizar gráficos e informações de ativos financeiros. O projeto inclui funcionalidades como a exibição de cotações, cálculo de dividendos e yields, e gráficos comparativos.

## Funcionalidades

- **Seleção de Ativo**: Permite ao usuário escolher ativos financeiros a partir de uma lista.
- **Exibição de Gráficos**: Mostra a cotação histórica do ativo selecionado utilizando gráficos interativos criados com `plotly`.
- **Cálculos de Dividendos**: Exibe os dividendos pagos nos últimos 12 meses e calcula os rendimentos do ativo, como `Dividend Yield` e `Yield on Cost`.
- **Comparação com Preço Médio**: Visualiza a comparação entre o preço atual e o preço médio do ativo ao longo do tempo.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação da interface da aplicação.
- **yfinance**: Biblioteca para obtenção de dados financeiros históricos de forma prática.
- **plotly**: Biblioteca para criação dos gráficos de cotação de ativos e dividendos.
- **pandas**: Biblioteca para análise, transformação e manipulação de dados.
- **numpy**: Biblioteca para operações numéricas e cálculo.
- **datetime**: Módulo para manipulação de data e hora.
- **requests**: Biblioteca para realizar requisições HTTP para a API yfinance.
- **time**: Módulo utilizado para verificações de expiração de cache após um período definido.

## Passos para Execução do Projeto

### 1. Clone o Repositório

Clone este repositório para sua máquina local:

```bash
git clone https://github.com/gilneifreitas/Projeto_Financas_ativos.git
cd Projeto_Financas_ativos
```


### 2. Crie e Ative um Ambiente Virtual (opcional, mas recomendado)

Para Windows:
```
python -m venv venv
.\venv\Scripts\activate
```
Para Linux/macOS:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto executando:
```
pip install -r requirements.txt
```

### 4. Execute o Aplicativo

Com todas as dependências instaladas, você pode iniciar o aplicativo Streamlit com o seguinte comando:
```
streamlit run interface.py
```
Seleção de Ativo:

Na barra lateral do aplicativo, você verá uma lista de ativos financeiros disponíveis. Selecione o ativo desejado.
Visualização do Gráfico:

Após a seleção do ativo, um gráfico interativo será exibido na tela com a cotação histórica do ativo selecionado.
Cálculos de Dividendos e Yield:

O aplicativo exibirá os dividendos pagos nos últimos 12 meses e os cálculos de rendimento como Dividend Yield e Yield on Cost.
Comparação de Preço:

O preço atual do ativo será comparado com o preço médio ao longo do tempo, e o gráfico mostrará essas informações de maneira clara.

Tabela resumo com os calculos de indicadores financeiros de dividendos e yields (DY e YOC), para a lista de ativos.


### Descrição dos Diretórios e Arquivos

- `data/`: Contém os arquivos de dados brutos ou tratados, como planilhas com histórico de dividendos e cotações organizadas.
- `src/`: Scripts auxiliares que realizam o carregamento, tratamento e geração de visualizações dos dados.
  - `grafico.py`: Responsável pela geração de gráficos financeiros.
  - `tabela.py`: Cria tabelas de resumo dos ativos.
  - `ativos_precos.py`: Define as listas de ativos e seus preços médios.
  - `carrega_dados.py`: Função central para carregar dados localmente ou online.
  - `dados_online.py`: Faz a requisição dos dados no Yahoo Finance e estrutura o DataFrame.
  - `salva_cotacao.py`: Salva os dados coletados de cotações e dividendos.
- `interface.py`: Script principal da aplicação, com a interface desenvolvida em Streamlit.
- `requirements.txt`: Lista das bibliotecas necessárias para execução do projeto.
- `.gitignore`: Especifica arquivos e pastas que devem ser ignorados pelo Git (ex: dados sensíveis).
- `README.md`: Este arquivo, que documenta a estrutura e finalidade do projeto.


### Estrutura do Projeto
A estrutura de diretórios do projeto é a seguinte:

```
Projeto_Financas_ativos/
│
├── data/ # Pasta para armazenar os dados
│ ├── dados_organizados.xlsx
│ ├── historico_dividendos.xlsx
│
├── src/ # Scripts principais de manipulação e visualização
│ ├── grafico.py # Gera os gráficos
│ ├── tabela.py # Gera tabela de resumo
│ ├── ativos_precos.py # Lista de ativos e preços médios
│ ├── carrega_dados.py # Carrega cotações e dividendos (online ou local)
│ ├── dados_online.py # Busca ativos no Yahoo Finance (formato: date|ticker|valor)
│ ├── salva_cotacao.py # Salva arquivos de cotação e dividendos
│
├── interface.py # Interface principal com Streamlit
├── requirements.txt # Lista de dependências do projeto
├── .gitignore # Arquivos e pastas ignoradas pelo Git
├── README.md # Documentação do projeto
```