# Métricas de competitividade de campeonatos de pontos corridos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from recursos import Bases

bases = Bases()
# Adicionar outras informações relevantes, como número de times, formato do campeonato, etc.
# Bem como os dados pré 2003
st.divider()

df = bases.ler('TabelaFinal.xlsx', 'br')

temporadas = df['CAMPEONATO'].unique()
data_por_temporada = [df[df['CAMPEONATO'] == temp]['PONTOS'] for temp in temporadas]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "História",
    "Boxplot de Pontos",
    "Gap do Campeão",
    "Desvio e Coef. de Variação",
    "Índice de Gini",
    "Índice Combinado"])

with tab1:
    st.write("""
    #### Análise geral do campeonato brasileiro de pontos corridos (2003-2025)
    
    O objetivo é fornecer métricas sobre a competitividade do campeonato ao\
    longo dos anos, utilizando diversas estatísticas.

    As análises incluem:
    - **Boxplot de Pontos por Temporada**: Visualização da distribuição de pontos dos times em cada temporada.
    - **Gap do Campeão**: Diferença de pontos entre o campeão e o vice-campeão em cada temporada.
    - **Desvio Padrão e Coeficiente de Variação**: Medidas de dispersão dos pontos para avaliar a competitividade.
    - **Índice de Gini**: Medida de desigualdade na distribuição de pontos entre os times.
    - **Índice Combinado de Competitividade**: Uma métrica composta que integra várias medidas para avaliar a competitividade geral do campeonato.

    Explore as abas acima para visualizar cada análise detalhadamente.
    """)

    # df_metrics = pd.DataFrame({
    #     "CAMPEONATO": temporadas,
    #     "Desvio": desvios,
    #     "Gap_Campeao": gap_campeao,
    #     "Gini": gini_temporadas,
    #     "Competitividade": competitividade
    # })
    # st.dataframe(df_metrics)

with tab2:
    #st.write("#### Boxplot de Pontos por Temporada")
    fig = px.line(df, x = "CAMPEONATO", y = "PONTOS", color = "CAMPEONATO",
              title = "Desempenho por temporada",
              markers = True,              
              labels = {"CAMPEONATO": "Temporada",
                        "PONTOS": "Pontos"})

    fig.update_traces(line = {'width':.7})
    st.plotly_chart(fig, theme = None, width = 'stretch')

with tab3:
    #st.write("#### Distância entre campeão e o vice")
    gap_campeao = []
    for temp in temporadas:
        pontos = df[df['CAMPEONATO'] == temp]['PONTOS'].sort_values(ascending=False).values
        gap_campeao.append(pontos[0] - pontos[1])

    fig = px.bar(
        x=temporadas, y=gap_campeao, title="Gap do Campeão em Cada Temporada",
        labels={"x": "Temporada", "y": "Vantagem do Campeão"})
    st.plotly_chart(fig, theme=None, width='stretch')

with tab4:
    #st.write("#### Desvio padrão e coeficiente de variação dos pontos")
    desvios = [np.std(df[df['CAMPEONATO']==temp]['PONTOS']) for temp in temporadas]
    media = [np.mean(df[df['CAMPEONATO']==temp]['PONTOS']) for temp in temporadas]
    coef_var = [d/m for d,m in zip(desvios, media)]

    fig = px.line(x=temporadas, y=desvios,
                  title="Desvio Padrão por Temporada", markers=True,
                  labels={"x": "Temporada", "y": "Desvio Padrão"})
    fig.add_scatter(x=temporadas, y=coef_var, mode='lines+markers',
                    name="Coeficiente de variação")
    st.plotly_chart(fig, theme=None, width='stretch')

with tab5:
    #st.write("#### Índice de Gini dos pontos por temporada")
    def gini(array):
        array = np.sort(array)
        n = len(array)
        return (2 * np.sum((np.arange(1, n+1) * array))) / (n * np.sum(array)) - (n + 1) / n

    gini_temporadas = [gini(df[df['CAMPEONATO']==temp]['PONTOS'].values) for temp in temporadas]

    fig = px.line(x=temporadas, y=gini_temporadas,
                  title="Índice de Gini por Temporada",
              labels={"x": "Temporada", "y": "Índice de Gini"})
    st.plotly_chart(fig, theme=None, width='stretch')

with tab6:
    #st.write("#### Índice combinado de competitividade")
    # Normaliza métricas
    metrics = np.array([desvios, gap_campeao, gini_temporadas]).T
    scaler = MinMaxScaler()
    metrics_scaled = scaler.fit_transform(metrics)

    # Competitividade = 1 - média das métricas de desigualdade
    competitividade = 1 - np.mean(metrics_scaled, axis=1)

    fig = px.line(x=temporadas, y=competitividade,
                  title="Índice Combinado de Competitividade por Temporada",
                  labels={"x": "Temporada", "y": "Competitividade"})
    st.plotly_chart(fig, theme=None, width='stretch')
