import numpy as np
import streamlit as st
import pandas as pd
import conversoes as cvs
import calendar
import filtrar_meses as fm
from filtro_completo import filter_dataframe


st.header("DASHBOARD")
st.header("Estatística de Alunos na Biblioteca")

# Limpeza de dados
base_dados_csv = pd.read_csv('Banco_de_Dados.csv').drop(columns=['Mês','Ano'])
base_dados_csv.columns = base_dados_csv.columns.str.strip()
base_dados_csv['Categoria'] = base_dados_csv['Categoria'].str.strip()
pd_dados_com_date= cvs.converter_coluna_data_em_datatime(base_dados_csv,'Data')

# Exibir tabela
st.dataframe(pd_dados_com_date)   

# Obter os meses do ano
meses = [item.upper() for item in calendar.month_abbr]
anos = pd_dados_com_date['Data'].apply(lambda data: data.year).unique()


# Criar o multiselect do filtro
multiselect_meses = st.sidebar.multiselect(
    "Filtro de meses",
    tuple(meses)
)
multiselect_years = st.sidebar.multiselect(
    "Filtro de Anos",
    tuple(anos)
)
# Criar um groupby passando a coluna para filtrar, a coluna para somar e os critérios
monthly_group = fm.count_sum_group_by_month(pd_dados_com_date, 'Data', 'Contagem', months=multiselect_meses)

# Exibir o groupby
col1, col2 = st.columns([1, 3])
col1.markdown('### Filtro por meses')
col1.dataframe(monthly_group) 
col2.markdown('### Gráfico')  
col2.bar_chart(monthly_group)

'### Filtro de soma de alunos por Categoria'
filt_soma_alunos = fm.count_sum_group_by_month_by_category(pd_dados_com_date, 'Data', 'Contagem',months=multiselect_meses)

st.dataframe(filt_soma_alunos)

filter_students_sum_year_month = fm.count_sum_group_by_month_year_category(pd_dados_com_date, 'Data', 'Contagem',months=multiselect_meses, years=multiselect_years)

st.bar_chart(filter_students_sum_year_month)







#st.dataframe(filter_dataframe(df))
