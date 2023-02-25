# importando as bibliotecas necessárias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


# importando os dados
dados = pd.read_csv('C:\dev\Streamlit-CAGED\data\CAGED-PE_LIMPO.csv')

# Centraliza o título utilizando HTML
st.write("<h1 style='text-align: center;'>Dashboard do CAGED-PE</h1>", unsafe_allow_html=True)




