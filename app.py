import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# localização para português
st.set_page_config(
    page_title="Dashboard CAGED Pernambuco",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# base de dados
file_path = 'https://github.com/Taciana3090/CAGED-PE/raw/master/Data/CAGED-PE_LIMPO.csv'
@st.cache_data  # cache para evitar o carregamento repetido dos dados
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

df = load_data(file_path)

# renomeando as colunas
df.rename(columns={
    'uf': 'Estado',
    'município': 'Cidade',
    'idade': 'Idade',
    'raçacor': 'Raça/Cor',
    'cbo2002ocupação': 'Código Ocupação',
    'categoria': 'Categoria',
    'graudeinstrução': 'Nível Instrução',
    'sexo': 'Gênero',
    'tipoempregador': 'Tipo Empregador',
    'tipoestabelecimento': 'Tipo Estabelecimento',
    'tipomovimentação': 'Tipo Movimentação',
    'tipodedeficiência': 'Tipo Deficiência',
    'indtrabintermitente': 'Trabalho Intermitente',
    'indtrabparcial': 'Trabalho Parcial',
    'salário': 'Salário',
    'seção': 'Seção de Atividade Econômica',
    'valorsaláriofixo': 'Valor Salário Fixo',
    'ano_declaração': 'Ano Declaração',
    'mês_declaração': 'Mês Declaração',
    'ano_exclusão': 'Ano Exclusão',
    'mês_exclusão': 'Mês Exclusão',
}, inplace=True)

# centralizando o título com HTML
st.write("<h1 style='text-align: center;'>Dashboard Interativo - Dados do CAGED-PE</h1>", unsafe_allow_html=True)
st.write("""

Bem-vindo ao nosso dashboard interativo! Aqui, você pode explorar análises detalhadas dos dados de empregos formais em Pernambuco.

**Objetivo:** Este dashboard tem como objetivo oferecer insights valiosos a partir dos dados do CAGED-PE, permitindo uma análise personalizada dos empregos formais na região.

**Exploração Interativa:** Use os filtros à esquerda para personalizar a visualização dos gráficos abaixo. Selecione o ano, a cidade, o gênero e a seção de atividade econômica para analisar diferentes aspectos dos dados.

**Gráficos:** Abaixo, você encontrará gráficos interativos que ilustram as tendências e os padrões dos empregos formais em Pernambuco.
""")

# lista de anos únicos
anos_disponiveis = df['Ano Declaração'].unique()

with st.sidebar:
    st.header("Filtros")
    st.markdown("Personalize a visualização dos gráficos:")
    selected_ano = st.radio('Ano:', anos_disponiveis)
    selected_cidade = st.selectbox('Cidade:', df['Cidade'].unique())
    selected_genero = st.selectbox('Gênero:', df['Gênero'].unique())
    selected_secao = st.selectbox('Seção de Atividade Econômica:', df['Seção de Atividade Econômica'].unique())


# base nos filtros selecionados
filtered_data = df[
    (df['Cidade'] == selected_cidade) &
    (df['Gênero'] == selected_genero) &
    (df['Seção de Atividade Econômica'] == selected_secao) &
    (df['Ano Declaração'] == selected_ano)
]

# histograma de Idades por Gênero
fig = px.histogram(
    filtered_data,
    x='Idade',
    color='Gênero',
    facet_col='Seção de Atividade Econômica',  # Facetamento por seção de atividade econômica
    title=f'Distribuição de Idades por {selected_genero} em {selected_cidade} ({selected_ano})',
    labels={'Idade': 'Idade', 'count': 'Número de Pessoas'} 
)

# seção de atividade econômica e tipo de movimentação (admissão/desligamento)
movimentacao_data = filtered_data.groupby(['Seção de Atividade Econômica', 'saldomovimentação', 'Gênero']).size().reset_index(name='Quantidade')

# gráfico de barras empilhadas para admissões e desligamentos
stacked_bar_chart = px.bar(
    movimentacao_data,
    x='Seção de Atividade Econômica',
    y='Quantidade',
    color='saldomovimentação',
    title=f'Admissões e Desligamentos por {selected_genero} em {selected_cidade} ({selected_ano})',
    labels={'Seção de Atividade Econômica': 'Seção de Atividade Econômica', 'Quantidade': 'Quantidade', 'saldomovimentação': 'Movimentação'}
)
# ...

# seção de atividade econômica, nível de instrução e tipo de movimentação (admissão/desligamento)
movimentacao_data = filtered_data.groupby(['Seção de Atividade Econômica', 'Nível Instrução', 'saldomovimentação']).size().reset_index(name='Quantidade')

# admissões e desligamentos
admissoes = movimentacao_data[movimentacao_data['saldomovimentação'] == 'Admissão']
desligamentos = movimentacao_data[movimentacao_data['saldomovimentação'] == 'Desligamento']

# gráfico de barras agrupadas para admissões e desligamentos por nível de instrução
grouped_bar_chart_movimentacao = px.bar(
    movimentacao_data,
    x='Seção de Atividade Econômica',
    y='Quantidade',
    color='Nível Instrução',
    barmode='group',  # modo de agrupamento de barras
    facet_col='saldomovimentação',
    title=f'Admissões e Desligamentos por {selected_genero} e Nível de Instrução em {selected_cidade} ({selected_ano})',
    labels={'Seção de Atividade Econômica': 'Seção de Atividade Econômica', 'Quantidade': 'Quantidade', 'saldomovimentação': 'Movimentação'}
)

# seção de atividade econômica, raça/cor e calcular a média salarial
media_salarial_por_secao_raca = filtered_data.groupby(['Seção de Atividade Econômica', 'Raça/Cor'])['Salário'].mean().reset_index()

# gráfico de barras facetado para a média salarial por setor de atividade econômica e raça/cor
bar_chart_media_salarial_raca = px.bar(
    media_salarial_por_secao_raca,
    x='Raça/Cor',
    y='Salário',
    color='Raça/Cor',
    facet_col='Seção de Atividade Econômica',  # Facetado por setor de atividade econômica
    facet_col_wrap=1,  # Uma coluna de subgráficos
    title=f'Média Salarial por {selected_genero} e Raça/Cor em {selected_cidade} ({selected_ano})',
    labels={'Raça/Cor': 'Raça/Cor', 'Salário': 'Média Salarial (R$)'}
)

# em reais no formato correto
bar_chart_media_salarial_raca.update_layout(yaxis_tickformat=',.2f')


# seção de atividade econômica, nível de instrução e calcular a média salarial
media_salarial_por_secao_instrucao = filtered_data.groupby(['Seção de Atividade Econômica', 'Nível Instrução'])['Salário'].mean().reset_index()

# gráfico de barras facetado para a média salarial por setor de atividade econômica e nível de instrução
bar_chart_media_salarial_instrucao = px.bar(
    media_salarial_por_secao_instrucao,
    x='Nível Instrução',
    y='Salário',
    color='Nível Instrução',
    facet_col='Seção de Atividade Econômica',  # Facetado por setor de atividade econômica
    facet_col_wrap=1,  # Uma coluna de subgráficos
    title=f'Média Salarial por {selected_genero} e Nível de Instrução em {selected_cidade} ({selected_ano})',
    labels={'Nível Instrução': 'Nível de Instrução', 'Salário': 'Média Salarial (R$)'}
)

# atividade econômica e tipo de deficiência
deficiencia_data = filtered_data.groupby(['Seção de Atividade Econômica', 'Tipo Deficiência']).size().reset_index(name='Quantidade')
bar_chart_deficiencia = px.bar(
    deficiencia_data,
    x='Seção de Atividade Econômica',
    y='Quantidade',
    color='Tipo Deficiência',
    barmode='group', 
    title=f'Distribuição de Tipos de Deficiência por {selected_genero} em {selected_cidade} ({selected_ano})',
    labels={'Seção de Atividade Econômica': 'Seção de Atividade Econômica', 'Quantidade': 'Quantidade', 'Tipo Deficiência': 'Tipo de Deficiência'}
)
# tipo de movimentação (admissão/demissão) e categoria de emprego
movimentacao_category = filtered_data.groupby(['Tipo Movimentação', 'Seção de Atividade Econômica']).size().reset_index(name='Quantidade')
stacked_bar_movimentacao_category = px.bar(
    movimentacao_category,
    x='Seção de Atividade Econômica',
    y='Quantidade',
    color='Tipo Movimentação',
    barmode='group', 
    title=f'Admissões e Demissões de {selected_genero} por Tipo de Movimentação e Categoria de Emprego em {selected_cidade} ({selected_ano})',
    labels={'Seção de Atividade Econômica': 'Categoria de Emprego', 'Quantidade': 'Quantidade', 'Tipo Movimentação': 'Tipo de Movimentação'}
)
# idades em intervalos
def age_group(age):
    if age < 25:
        return '<25'
    elif age < 35:
        return '25-34'
    elif age < 45:
        return '35-44'
    elif age < 55:
        return '45-54'
    else:
        return '55+'

filtered_data['Faixa Etária'] = filtered_data['Idade'].apply(age_group)
# dados por gênero, faixa etária e ano e calcular a taxa de desemprego
unemployment_data = filtered_data.groupby(['Gênero', 'Faixa Etária', 'Ano Declaração'])['saldomovimentação'].apply(lambda x: (x == 'Desligamento').sum()).reset_index(name='Desempregados')
total_people_data = filtered_data.groupby(['Gênero', 'Faixa Etária', 'Ano Declaração'])['saldomovimentação'].count().reset_index(name='Total')
# desempregados e total de pessoas
unemployment_rate_data = unemployment_data.merge(total_people_data, on=['Gênero', 'Faixa Etária', 'Ano Declaração'])
# taxa de desemprego
unemployment_rate_data['Taxa de Desemprego'] = (unemployment_rate_data['Desempregados'] / unemployment_rate_data['Total']) * 100
bar_unemployment_rate = px.bar(
    unemployment_rate_data,
    x='Faixa Etária',
    y='Taxa de Desemprego',
    color='Gênero',
    title=f'Taxa de Desemprego por {selected_genero} e Faixa Etária em {selected_cidade}',
    labels={'Faixa Etária': 'Faixa Etária', 'Taxa de Desemprego': 'Taxa de Desemprego (%)', 'Gênero': 'Gênero'},
    facet_col='Ano Declaração' 
)

# em reais no formato correto
bar_chart_media_salarial_instrucao.update_layout(yaxis_tickformat=',.2f')

# gráficos na página principal
st.write("<h2 style='text-align: center;'>Gráficos</h2>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)  
st.plotly_chart(stacked_bar_chart, use_container_width=True)  
st.plotly_chart(grouped_bar_chart_movimentacao, use_container_width=True)
st.plotly_chart(bar_chart_media_salarial_raca, use_container_width=True)
st.plotly_chart(bar_chart_media_salarial_instrucao, use_container_width=True)
st.plotly_chart(bar_chart_deficiencia, use_container_width=True)
st.plotly_chart(stacked_bar_movimentacao_category, use_container_width=True)
st.plotly_chart(bar_unemployment_rate, use_container_width=True)

