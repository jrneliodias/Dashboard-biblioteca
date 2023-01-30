import numpy as np
import streamlit as st
import pandas as pd
from calendar import month_abbr
from filtrar_meses import *
from Limpeza_dados import *
from filtro_completo import filter_dataframe
import plotly.express as px

st.set_page_config(layout="wide")
st.header("DASHBOARD")
st.header("Estatística de Alunos na Biblioteca")

# Limpeza de dados
pd_dados_date = limpar_dados(file_path='Banco_de_Dados.csv',
                             columns_to_drop=['Mês', 'Ano'], change_date=True)
dados_df = limpar_dados(file_path='Banco_de_Dados.csv',
                        columns_to_drop=['Mês', 'Ano'])

# Exibir tabela
st.checkbox("Expandir Tabela", value=False, key="use_container_width")

st.dataframe(
    pd_dados_date, use_container_width=st.session_state.use_container_width)

# Obter os meses do ano
meses = [item.upper() for item in month_abbr]
anos = pd_dados_date['Data'].apply(lambda data: data.year).unique()


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
monthly_group = count_sum_group_by_month(
    pd_dados_date, 'Data', 'Contagem', months=multiselect_meses)

# Exibir o groupby
st.markdown('### Total de usuários por mês')
col1, col2 = st.columns([1, 3])

col1.dataframe(monthly_group, use_container_width=True)
col2.bar_chart(monthly_group)

'### Filtro de soma de alunos por Categoria'
filt_soma_alunos = count_sum_group_by_month_by_category(
    pd_dados_date, 'Data', 'Contagem', months=multiselect_meses)

filter_students_sum_year_month = count_sum_group_by_month_year_category(
    dados_df, 'Data', 'Contagem', months=multiselect_meses, years=multiselect_years)

col3, col4 = st.columns([1, 3])
col3.dataframe(filt_soma_alunos)
col4.bar_chart(filter_students_sum_year_month)

##
fig = px.histogram(filter_students_sum_year_month, x=filter_students_sum_year_month.index,
                   y=filter_students_sum_year_month.columns,
                   labels={'y': 'Soma de Alunos', 'x': 'Meses'},
                   barmode='group',
                   text_auto='.2s',
                   )
fig.update_layout(legend_title_text='Categoria',
                  legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=-0.3,
                      xanchor="right",
                      x=1,

                  ))

###
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

temp = dados_df['Data'].apply(lambda x: month_abbr[x.month].upper())
temp


# st.dataframe(filter_dataframe(df))
