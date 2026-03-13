# Baixar dados
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql

def ler_sql(tabela, user = st.secrets.connections.mysql.username,
            password = st.secrets.connections.mysql.password,
            host = '100.102.149.26', port = 3306, database = 'REFB'):
    """Lê uma tabela do banco de dados e retorna um DataFrame."""

    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    sql_query = f'SELECT * FROM {tabela}'
    df = pd.read_sql(sql_query, con=engine)
    
    return df


st.divider()

st.markdown(('### Baixar dados'))

st.markdown('Os dados utilizados para a construção do REFB podem ser baixados \
            integralmente nesta página, permitindo que pesquisadores, analistas \
            e entusiastas do futebol possam acessar as informações de forma \
            direta e utilizá-las para suas próprias análises, projetos ou estudos.')

st.markdown('Caso seja necessário, é possível fazer uma seleção manual da tabela.')

lista = {'Campeonato brasileiro fase inicial (2001-2002)':'mm_fase_inicial',
         'Campeonato brasileiro fase final (2001-2002)':'mm_fase_final',
         'Campeonato brasileiro pontos corridos (2003-2025) ':'pontoscorridos'}

opcao =  st.selectbox('Selecione a tabela', lista.keys(),
                      #placeholder = "Selecione uma tabela",
                      label_visibility = 'collapsed')

st.divider()

conectar = st.connection('mysql', type='sql')

dfquery = conectar.query('SELECT * FROM mm_fase_final;', ttl=600)

st.dataframe(dfquery,
             column_config = {
                    'campeonato': st.column_config.TextColumn("Campeonato"),
                    'fase': st.column_config.TextColumn("Fase"),
                    'data': st.column_config.TextColumn("Data"),
                    'temporada': st.column_config.NumberColumn("Temporada"),
                    'rodada': st.column_config.NumberColumn("Rodada"),
                    'jogo': st.column_config.TextColumn("Jogo"),
                    'time_mandante': st.column_config.TextColumn("Time mandante"),
                    'time_visitante': st.column_config.TextColumn("Time visitante"),
                    'gols_mandante': st.column_config.NumberColumn("Gols mandante"),
                    'gols_visitante': st.column_config.NumberColumn("Gols visitante"),

                    'pontos_mandante': st.column_config.NumberColumn("Pontos mandante"),
                    'pontos_visitante': st.column_config.NumberColumn("Pontos visitante"),
                    'detalhes': st.column_config.TextColumn("Detalhes")
                })
