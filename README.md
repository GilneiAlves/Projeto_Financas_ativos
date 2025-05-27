# Análise de Ativos com Streamlit e yFinance
# https://gilneialvesfinancas.streamlit.app/

Este projeto realiza a análise de ativos financeiros utilizando a biblioteca `yfinance` para buscar dados históricos de ações e o `Streamlit` para criar uma interface interativa que permite visualizar gráficos e informações de ativos financeiros. O projeto inclui funcionalidades como a exibição de cotações, cálculo de dividendos e yields, e gráficos comparativos.

## Motivação e Contexto

No dinâmico mercado financeiro, acompanhar o desempenho de ativos, especialmente com foco em dividendos e custo de aquisição, pode exigir o uso de múltiplas plataformas ou planilhas complexas. Este projeto nasceu com o objetivo de **centralizar e simplificar essas análises** em uma interface web interativa e intuitiva.

Além de resolver uma necessidade prática de visualização de portfólio, o desenvolvimento desta aplicação serviu como uma excelente oportunidade para aplicar e aprofundar conhecimentos em **Python para finanças**, explorando o poder do `yfinance` para coleta de dados em tempo real (ou quase) e do `Streamlit` para a construção de *data apps* de forma ágil e eficiente.

## Funcionalidades

- **Seleção de Ativo**: Permite ao usuário escolher ativos financeiros a partir de uma lista.
- **Exibição de Gráficos**: Mostra a cotação histórica do ativo selecionado utilizando gráficos interativos criados com `plotly`.
- **Cálculos de Dividendos**: Exibe os dividendos pagos nos últimos 12 meses e calcula os rendimentos do ativo, como `Dividend Yield` e `Yield on Cost`.
- **Comparação com Preço Médio**: Visualiza a comparação entre o preço atual e o preço médio do ativo ao longo do tempo.

## Exemplos de Uso e Análise

Com esta ferramenta, é possível obter insights rápidos como:

* **Visualizar Tendências:** Acompanhe a evolução da cotação de um ativo (ex: `MXRF11.SA`) ao longo do tempo e identifique visualmente períodos de alta, baixa ou consolidação.
* **Analisar Renda Passiva:** Verifique o total de dividendos pagos por uma ação (ex: `HGRU11.SA`) nos últimos 12 meses e calcule seu `Dividend Yield` (DY) para entender o retorno atual em relação ao preço.
* **Avaliar Custo vs. Valor:** Compare seu preço médio de aquisição com a cotação atual de um ativo (ex: `KNCR11.SA`) através do gráfico e do `Yield on Cost` (YOC), avaliando a performance real do seu investimento inicial.
* **Visão Rápida da Carteira:** Utilize a tabela resumo para comparar rapidamente os indicadores de DY e YOC de todos os seus ativos listados, facilitando a identificação de quais estão gerando mais retorno sobre o custo.

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
git clone https://github.com/GilneiAlves/Projeto_Financas_ativos.git
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


## Próximos Passos

Este projeto está em constante evolução. Algumas ideias para futuras implementações incluem:

* **Adicionar Mais Indicadores:** Incluir métricas fundamentalistas importantes como P/L (Preço/Lucro), P/VP (Preço/Valor Patrimonial), ROE (Retorno sobre Patrimônio Líquido), etc.
* **Gerenciamento de Portfólio:** Permitir que o usuário insira suas transações de compra/venda para um cálculo automático e mais preciso do preço médio e da performance da carteira.
* **Notícias e Alertas:** Integrar notícias relevantes para os ativos selecionados ou criar um sistema de alertas de preço ou distribuição de dividendos.
* **Suporte a Outros Ativos:** Expandir a análise para incluir Ações brasileiras, Ações Internacionais ou Criptomoedas.
* **Testes Automatizados:** Implementar testes unitários e de integração para garantir a robustez do código.

Entre em contato <https://www.linkedin.com/in/gilnei-freitas/> para recomendar uma nova funcionalidade ou relatar um erro ou inconsistências.
