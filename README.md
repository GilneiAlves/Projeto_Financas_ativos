# Análise de Ativos com Streamlit e yFinance
# https://gilneialvesfinancas.streamlit.app/

Este projeto realiza a análise de ativos financeiros utilizando a biblioteca `yfinance` para buscar dados históricos de ações e o `Streamlit` para criar uma interface interativa que permite visualizar gráficos e informações de ativos financeiros. O projeto inclui funcionalidades como a exibição de cotações, cálculo de dividendos e yields, e gráficos comparativos.

## Funcionalidades

- **Seleção de Ativo**: Permite ao usuário escolher ativos financeiros a partir de uma lista.
- **Exibição de Gráficos**: Mostra a cotação histórica do ativo selecionado utilizando gráficos interativos criados com `plotly`.
- **Cálculos de Dividendos**: Exibe os dividendos pagos nos últimos 12 meses e calcula os rendimentos do ativo, como `Dividend Yield` e `Yield on Cost`.
- **Comparação com Preço Médio**: Visualiza a comparação entre o preço atual e o preço médio do ativo ao longo do tempo.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web interativas em Python.
- **yfinance**: Biblioteca para buscar dados financeiros históricos.
- **plotly**: Biblioteca para criação de gráficos interativos.
- **pandas**: Biblioteca para análise e manipulação de dados.
- **numpy**: Biblioteca para operações numéricas.

## Passos para Execução do Projeto

### 1. Clone o Repositório

Clone este repositório para sua máquina local:

```bash
git clone https://github.com/gilneifreitas/ativosfinanceiros.git
cd ativosfinanceiros
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
streamlit run app.py
```
Seleção de Ativo:

Na barra lateral do aplicativo, você verá uma lista de ativos financeiros disponíveis. Selecione o ativo desejado.
Visualização do Gráfico:

Após a seleção do ativo, um gráfico interativo será exibido na tela com a cotação histórica do ativo selecionado.
Cálculos de Dividendos e Yield:

O aplicativo exibirá os dividendos pagos nos últimos 12 meses e os cálculos de rendimento como Dividend Yield e Yield on Cost.
Comparação de Preço:

O preço atual do ativo será comparado com o preço médio ao longo do tempo, e o gráfico mostrará essas informações de maneira clara.

### Estrutura do Projeto
A estrutura de diretórios do projeto é a seguinte:
```
├── app.py                  # Arquivo principal do Streamlit
├── requirements.txt        # Arquivo com as dependências do projeto
├── README.md               # Este arquivo
└── assets/                 # Diretório para arquivos estáticos (opcional)
```
