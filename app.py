# importando as bibliotecas necessárias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go



@st.cache_resource
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

file_path = 'https://github.com/Taciana3090/CAGED-PE/raw/master/Data/CAGED-PE_LIMPO.csv'
df = load_data(file_path)

# Centraliza o título utilizando HTML
st.write("<h1 style='text-align: center;'>Dashboard do CAGED-PE</h1>", unsafe_allow_html=True)
st.write("""
Este dashboard tem como objetivo apresentar uma análise dos dados do CAGED-PE. Os dados incluem informações sobre empregos formais em Pernambuco.
""")

# Criando uma cópia do dataframe com apenas as colunas desejadas
df_adm_desl = df[['município', 'saldomovimentação']]

# Agrupando por município e contando o número de admissões e desligamentos
df_adm_desl = df_adm_desl.groupby('município')['saldomovimentação'].value_counts().unstack()

# Calculando o total de movimentações (admissões + desligamentos) para cada município
df_adm_desl['total'] = df_adm_desl.sum(axis=1)

# Ordenando os municípios pelo total de movimentações
df_adm_desl = df_adm_desl.sort_values('total', ascending=False)

# Selecionando apenas os 10 primeiros municípios
df_adm_desl = df_adm_desl.head(10)

# Criando a figura do gráfico
fig = go.Figure()

# Adicionando as barras empilhadas de admissões e desligamentos
fig.add_trace(go.Bar(
    y=df_adm_desl.index,
    x=df_adm_desl['Admissão'],
    orientation='h',
    name='Admissões',
    marker=dict(color='#1f77b4')
))

fig.add_trace(go.Bar(
    y=df_adm_desl.index,
    x=-df_adm_desl['Desligamento'],
    orientation='h',
    name='Desligamentos',
    marker=dict(color='#ff7f0e')
))

# Personalizando o layout do gráfico
fig.update_layout(
    title='10 Municípios com mais Admissões e Desligamentos entre 2020-2022',
    xaxis_title='Número de trabalhadores',
    yaxis_title='Município',
    barmode='overlay',
    bargap=0.1,
    bargroupgap=0.1,
    template='plotly_white'
)

# Exibindo o gráfico
st.plotly_chart(fig)


# Selecionar apenas as colunas relevantes para o dashboard
cols = ["seção", "salário", "tipomovimentação", "sexo", "saldomovimentação", "idade", "graudeinstrução"
        , "raçacor", "ano_declaração", "mês_declaração", "município"]
df = df[cols]


# Converter o tipo de dados da coluna "salário" para float e formatar a coluna
df["salário"] = df["salário"].astype(str).replace(',', '').replace('.', '').astype(float)


# Agrupar os dados por setor da economia e calcular as estatísticas relevantes
grouped = df.groupby(["seção"]).agg({
    "salário": ["mean", "median", "min", "max"],
    "tipomovimentação": ["count"]
})

# Renomear as colunas para uma melhor legibilidade
grouped.columns = ["_".join(col).strip() for col in grouped.columns.values]

# Agrupar os dados por setor da economia e calcular a média salarial
grouped = df.groupby(["seção"]).agg({
    "salário": "mean"
}).reset_index()

# Criar o gráfico de barras com a média salarial por setor da economia
chart = alt.Chart(grouped).mark_bar().encode(
    x=alt.X('salário:Q', title='Média Salarial', axis=alt.Axis(format='$.2f')),
    y=alt.Y('seção:N', title='Setor da Economia'),
    color=alt.Color('seção:N', legend=None)
).properties(
    width=600,
    height=400,
    title='Média Salarial por Setor da Economia em Pernambuco'
)

# Exibir o gráfico
st.altair_chart(chart, use_container_width=True)

# Selecionar apenas as colunas relevantes para o dashboard
cols = ["sexo", "salário", "saldomovimentação"]
df = df[cols]

# Converter o tipo de dados da coluna "salário" para float e formatar a coluna
df["salário"] = df["salário"].astype(str).replace(',', '').replace('.', '').astype(float)

# Agrupar os dados por sexo e calcular a média salarial
grouped = df.groupby(["sexo"]).agg({
    "salário": "mean"
}).reset_index()

# Criar o gráfico de barras com a média salarial por sexo
color_scale = alt.Scale(domain=["Mulher", "Homem"], range=["#FF69B4", "#1E90FF"])
chart = alt.Chart(grouped).mark_bar().encode(
    x=alt.X('sexo:N', title='Sexo'),
    y=alt.Y('salário:Q', title='Média Salarial', axis=alt.Axis(format='$.2f')),
    color=alt.Color('sexo:N', scale=color_scale)
).properties(
    width=600,
    height=400,
    title='Média Salarial por Sexo em Pernambuco'
)

# Exibir o gráfico
st.altair_chart(chart, use_container_width=True)

