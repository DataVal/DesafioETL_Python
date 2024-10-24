# -*- coding: utf-8 -*-
"""DesafioETL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qjpgbSNjpUtpbx8ifusZM5Rn1eQ_6USz

**A /confidencial/ é um dos maiores Multifamily Offices do país, especializada na distribuição do portfólio de seus clientes entre diferentes ativos Onshore e Offshore.**

Neste teste, fornecido via e-mail junto com o dataset nomeado `Dataset_Teste_Python`, você deverá analisar os dados disponibilizados e responder às perguntas que se seguem.

Este dataset detalha o patrimônio no Brasil e no exterior, por integrante de família, com atualizações diárias ao longo do ano de 2023. Além disso, fornece informações detalhadas sobre as estratégias de alocação. As estratégias Onshore são identificadas pelo sufixo (ON) nas colunas, enquanto as estratégias Offshore apresentam o sufixo (OFF). Todos os valores estão expressos em reais (R$).

Todas as estratégias são monitoradas por um sistema proprietário da /confidencial/, que acompanha a evolução das alocações para assegurar sua conformidade com os relatórios e extratos enviados pelos bancos custodiantes. As colunas intituladas Financeiro Banco seguidas pelo nome da estratégia indicam o patrimônio reportado pelo banco custodiante para a estratégia específica na data correspondente.

Este teste pode ser realizado utilizando principalmente as bibliotecas `pandas` e `numpy`. Contudo, fique à vontade para empregar quaisquer outras bibliotecas que julgar necessárias.
"""

import pandas as pd
import numpy as np

"""**Questão 1**: Importação do Dataset

Importe o dataset `Dataset_Teste_Python` para este notebook. Utilize as bibliotecas necessárias para a leitura do arquivo. Lembre-se de que, neste caso, não é necessário se preocupar com o caminho específico do arquivo no seu computador; a avaliação se concentrará na abordagem adotada para a importação.
"""

# Insira seu código aqui para importar o dataset
import chardet
path = '/content/Dataset_Teste_Python(in).csv'
# Aqui eu to basicamente descobrindo qual é o encoding para ler corretamente o arquivo
with open(path, 'rb') as arquivocsv:
    resultadoEncd = chardet.detect(arquivocsv.read(10000))
# Agora eu uso o resultado no encoding, nesse caso acabou sendo o padrão latin1
data = pd.read_csv(path, encoding=resultadoEncd['encoding'])

"""**Questão 2.1:** Visualização do Dataset

Exiba as 10 primeiras e as 10 últimas linhas do dataset para entender a estrutura dos dados.
"""

# Insira seu código aqui para as 10 primeiras linhas
data.head(10)
# Insira seu código aqui para as 10 últimas linhas
data.tail(10)

# Mas no Jupyter ou no Colab pode ter um problema onde só a última tabela é exibida, resolvo isso com o seguinte código
dezprimeiras = data.head(10)
dezultimas = data.tail(10)
dezprimplusdezult = pd.concat([dezprimeiras, dezultimas])
dezprimplusdezult

"""**Questão 2.2:** Visualização do Dataset

Mostre quantas linhas e quantas colunas tem no dataset.
"""

# Insira seu código aqui para mostrar as dimensões do dataset
data.shape

"""**Questão 3**: Criação das Colunas de Conciliação.

Para cada par de colunas correspondente a uma estratégia e seu respectivo valor no financeiro do banco, crie uma nova coluna para conciliação. Esta coluna deve ser nomeada como 'Conciliação + Nome da Estratégia', e inicialmente estará vazia, pronta para receber os resultados de uma eventual conciliação.

Por exemplo, para a estratégia 'Renda Fixa (ON)', a nova coluna deve ser chamada 'Conciliação Renda Fixa (ON)'.
"""

# Insira seu código aqui para adicionar as colunas de conciliação ao dataset
colunas = data.columns[3::2]

for estrategia in colunas:
    conciliacao = 'Conciliação ' + estrategia
    data.insert(data.columns.get_loc(estrategia) + 1, conciliacao, None)

"""**Questão 4**: Realização da Conciliação.

A conciliação financeira é um processo crítico para assegurar a precisão entre os valores registrados internamente e aqueles reportados pelos bancos custodiantes. Este processo envolve comparar o patrimônio registrado no sistema da Turim com os valores fornecidos pelos bancos para cada estratégia de investimento. O objetivo é identificar e quantificar quaisquer discrepâncias entre estes valores.

Para cada estratégia de investimento, você deverá calcular a diferença entre o valor financeiro registrado no sistema da /confidencial/ ('Nome da Estratégia') e o valor correspondente informado pelo banco ('Financeiro Banco Nome da Estratégia'). Essa diferença deve ser registrada nas novas colunas de conciliação criadas anteriormente ('Conciliação Nome da Estratégia').
"""

# Insira seu código aqui para realizar a conciliação dos valores financeiros
colunas = data.columns[4::3]

for conciliacao in colunas:
    estrategia = data.columns.get_loc(conciliacao) - 1
    financeiro = data.columns.get_loc(conciliacao) + 1
    data[conciliacao] = data.iloc[:, estrategia] - data.iloc[:, financeiro]

"""**Questão 5**: Exiba as linhas com diferenças.

Após concluir o processo de conciliação, é importante focar naquelas divergências que excedem um limiar específico, indicando possíveis inconsistências significativas entre os registros internos e as informações fornecidas pelos bancos custodiantes.

Para esta etapa, filtre e exiba todas as linhas do dataset em que a conciliação de qualquer estratégia de investimento apresente uma divergência, em módulo, superior a R$10,00.
"""

# Insira seu código aqui para filtrar e exibir as linhas com divergências significativas
linhas_divergentes = data[(data[colunas].abs() > 10).any(axis=1)]
linhas_divergentes

"""**Questão 6**: Tratamento das divergências.

Quando divergências significativas são identificadas, é essencial aplicar correções para garantir a integridade e precisão dos dados financeiros registrados. Nesta etapa, você deverá atualizar o valor patrimonial na coluna de estratégia para cada caso onde a divergência excedeu o limiar estabelecido, utilizando como referência o valor informado pelo banco custodiante.

Para isso, substitua o valor na coluna de estratégia pelo valor correspondente na coluna de "Financeiro Banco" para todas as divergências superiores a R$10,00. Este procedimento visa alinhar os registros internos com as informações oficiais fornecidas pelos bancos, assegurando uma base de dados consistente e confiável.
"""

# Insira seu código aqui para realizar o tratamento das divergências
for conciliacao in colunas:
    financeiro = data.columns.get_loc(conciliacao) + 1
    estrategia = data.columns.get_loc(conciliacao) - 1
    filtro = data[conciliacao].abs() > 10
    data.loc[filtro, data.columns[estrategia]] = data.loc[filtro, data.columns[financeiro]]

"""**Questão 7**: Verificação de divergências após correção.

Após realizar o tratamento das divergências conforme instruído na questão anterior, é fundamental conferir se o processo de correção foi efetivamente bem-sucedido. Portanto, nesta etapa, você deve realizar novamente a busca por divergências superiores a R$10,00 entre as colunas de estratégia e as respectivas colunas de "Financeiro Banco". Se a correção foi realizada corretamente, esta nova verificação não deverá exibir nenhuma linha, indicando que todas as divergências significativas foram devidamente ajustadas.
"""

# Insira seu código aqui para verificar se ainda existem divergências superiores a R$10,00 após a correção
divergencias = []

for conciliacao in colunas:
    financeiro = data.columns.get_loc(conciliacao) + 1
    estrategia = data.columns.get_loc(conciliacao) - 1
    filtro = (data[data.columns[estrategia]] - data[data.columns[financeiro]]).abs() > 10
    divergencias.append(data[filtro])

divergencias_df = pd.concat(divergencias)
divergencias_df

"""**Questão 8**: Montagem do Extrato do Cliente

Para montar o extrato dos clientes, utilizaremos os dados financeiros contidos nas colunas de estratégia, focando especificamente nos valores registrados no último dia de cada mês do ano de referência. O objetivo é consolidar uma visão clara do patrimônio do cliente, estratégia por estratégia, ao final de cada período mensal.

Monte uma tabela que contenha apenas os dados financeiros de cada cliente no último dia de cada mês. (Não utilize as colunas de Financeiro Banco)
"""

# Insira seu código aqui para montar o extrato do cliente
data['Data'] = pd.to_datetime(data['Data'])
extrato = data[data['Data'].dt.is_month_end]

"""**Questão 9**: Tabela Resumo

Para finalizar, construiremos uma tabela resumo que consolida o financeiro por família, agregando os valores por estratégia de cada cliente pertencente a uma mesma família. Adicionalmente, incluiremos duas colunas: uma para o patrimônio total onshore (soma de todas as estratégias onshore por família) e outra para o patrimônio total offshore (soma de todas as estratégias offshore por família).
"""

# Insira seu código aqui para montar a tabela resumo
# Dicas:
# 1. Utilize a tabela obtida na questão anterior como base.
# 2. O resultado será uma tabela resumo com o financeiro consolidado por família, incluindo as colunas de patrimônio total onshore e offshore.

tabelaUltimoExtrato = extrato[extrato['Data'].dt.is_year_end].copy()
colunas_relevantes = tabelaUltimoExtrato.loc[:, ~tabelaUltimoExtrato.columns.str.contains('Financeiro|Conciliação')]

resumoPCliente = tabelaUltimoExtrato[colunas_relevantes.columns].copy()

resumoPCliente['Total_ON'] = resumoPCliente.filter(regex='ON').sum(axis=1)
resumoPCliente['Total_OFF'] = resumoPCliente.filter(regex='OFF').sum(axis=1)
resumoFinal = resumoPCliente.groupby('ID Família').sum(numeric_only=True).reset_index()

resumoFinal

"""# Pessoal
Achei um desafio muito interessante que me fez voltar lá pras minhas bases no segundo período da faculdade onde tive contato pela primeira vez com Python. A necessidade de criar filtros, agregações e manipular o dataset me deixou empolgado e curioso pra saber como é a rotina em uma empresa como a /confidencial/. Espero que os códigos tenham satisfeito o requisitado e adianto que estou muito empolgado para continuar aprendendo com situações reais como essa.
"""