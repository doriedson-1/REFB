# Baixar dados
import streamlit as st
import pandas as pd
import os
from recursos import Bases

# A commit '3277917' possui a versão da página com conexão MySQL.
# https://github.com/doriedson-1/REFB/commit/3277917edc01f88c52c3482a677baa1cae313f5b

def procurar_arq(nome):
    """
    Procura arquivos dentro da pasta principal 'Base_de_dados'.
    """
    root_dir = st.secrets.caminho_base_dados

    for root, dirs, files in os.walk(root_dir):
        if nome in files:
            return (os.path.join(root, nome))
        

def ler_outra(caminho):
    if caminho.split('.')[-1] == 'csv':
        try:
            # Tenta ler o arquivo CSV
            df = pd.read_csv(caminho)
            return df
        
        except FileNotFoundError:
            print("Arquivo não encontrado. Por favor, certifique-se que\
                        o arquivo está na pasta.")
            return pd.DataFrame()
    
    elif (caminho.split('.')[-1] == 'xlsx') or (caminho.split('.')[-1] == 'xls'):
        #print(caminho_cheio)
        try:
            # Tenta ler o arquivo excel
            df = pd.read_excel(caminho)
            return df
        except FileNotFoundError:
            print("Não encontrado!")

bases = Bases()

st.divider()

st.markdown(('### Baixar dados'))

st.markdown('Os dados utilizados para a construção do REFB podem ser baixados \
            integralmente nesta página, permitindo que pesquisadores, analistas \
            e entusiastas do futebol possam acessar as informações de forma \
            direta e utilizá-las para suas próprias análises, projetos ou estudos.')

st.markdown('Caso seja necessário, é possível fazer uma seleção manual da tabela.')

lista = {'Campeonato brasileiro: fase inicial (2001-2002)':'mm_fase_inicial.csv',
         'Campeonato brasileiro: fase final (2001-2002)':'mm_fase_final.csv',
         'Campeonato brasileiro: pontos corridos (2003-2025)':'pontos_corridos.xlsx',
         'Campeonato brasileiro: tabelas finais (2003-2025)':'TabelaFinal.xlsx',
         'Libertadores: confrontos entre brasileiros':'lib.xls'}

opcao =  st.selectbox('Selecione a tabela', lista.keys())

st.divider()

df = ler_outra(procurar_arq(lista[opcao]))

st.dataframe(df,
             column_config = {
                    'campeonato': st.column_config.TextColumn("Campeonato"),
                    'fase': st.column_config.TextColumn("Fase"),
                    'data': st.column_config.DateColumn("Data"),
                    'temporada': st.column_config.NumberColumn("Temporada"),
                    'rodada': st.column_config.NumberColumn("Rodada"),
                    'jogo': st.column_config.TextColumn("Jogo"),
                    'time_mandante': st.column_config.TextColumn("Time mandante"),
                    'time_visitante': st.column_config.TextColumn("Time visitante"),
                    'gols_mandante': st.column_config.NumberColumn("Gols mandante"),
                    'gols_visitante': st.column_config.NumberColumn("Gols visitante"),

                    'pontos_mandante': st.column_config.NumberColumn("Pontos mandante"),
                    'pontos_visitante': st.column_config.NumberColumn("Pontos visitante"),
                    'detalhes': st.column_config.TextColumn("Detalhes"),

                    'estadio': st.column_config.TextColumn("Estádio"),
                    'arbitro': st.column_config.TextColumn("Árbitro"),
                    'publico': st.column_config.TextColumn("Público"),
                    'publico_max': st.column_config.TextColumn("Público máx."),
                    'tecnico_mandante': st.column_config.TextColumn("Técnico mandante"),
                    'tecnico_visitante': st.column_config.TextColumn("Técnico visitante")
                },
                hide_index=True)

