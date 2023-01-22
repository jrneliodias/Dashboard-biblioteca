import numpy as np
import streamlit as st
import pandas as pd
import conversoes as cvs
import calendar
from filtrar_meses import count_sum_group_by_month
from filtro_completo import filter_dataframe


st.header("DASHBOARD")
st.header("Estatística de Alunos na Biblioteca")
df = pd.read_csv('Banco_de_Dados.csv')


df2= cvs.converter_coluna_data_em_datatime(df,'Data')
st.dataframe(df2)   

# Obter os meses do ano
meses = [item.upper() for item in calendar.month_abbr]

# Criar o multiselect do filtro
multiselect_meses = st.sidebar.multiselect(
    "Filtro de meses",
    tuple(meses)
)

# Criar um groupby passando a coluna para filtrar, a coluna para somar e os critérios
monthly_group = count_sum_group_by_month(df, 'Data', 'Contagem', months=multiselect_meses)

# Exibir o groupby
col1, col2 = st.columns([1, 3])
col1.markdown('### Filtro por meses')
col1.dataframe(monthly_group) 
col2.markdown('### Gráfico')  
col2.bar_chart(monthly_group)

#st.dataframe(filter_dataframe(df))
    