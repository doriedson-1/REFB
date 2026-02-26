# Métricas de competitividade de campeonatos de pontos corridos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from recursos import Bases

def gini(array):
    array = np.sort(array)
    n = len(array)
    return (2 * np.sum((np.arange(1, n+1) * array))) / (n * np.sum(array)) - (n + 1) / n

def minmax_escala(vetor):
    return (vetor - np.min(vetor, axis=0)) / (np.max(vetor, axis=0) - np.min(vetor, axis=0))

bases = Bases()
# Adicionar outras informações relevantes, como número de times, formato do campeonato, etc.
# Bem como os dados pré 2003
st.divider()

df = bases.ler('TabelaFinal.xlsx', 'br')

temporadas = df['CAMPEONATO'].unique()
data_por_temporada = [df[df['CAMPEONATO'] == temp]['PONTOS'] for temp in temporadas]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "História",
    "Indice de Gini",
    "Vantagem do campeão",
    "Desvio padrão",
    "Boxplot de pontos",
    "Índice combinado"])

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
    #st.write("#### Índice de Gini dos pontos por temporada")
    gini_temporadas = [gini(df[df['CAMPEONATO']==temp]['PONTOS'].values) for temp in temporadas]

    st.markdown("O índice de Gini é uma medida de desigualdade. No contexto do \
                campeonato, um Gini mais baixo indica uma distribuição de pontos \
                mais equilibrada entre os times, sugerindo maior competitividade. \
                Já um Gini mais alto indica que poucos times concentram a maioria \
                dos pontos, sugerindo menor competitividade.")
    st.markdown("- O índice varia de 0 a 1, onde 0 representa perfeita igualdade \
                (todos os times têm os mesmos pontos) e 1 representa máxima \
                desigualdade (um time tem todos os pontos e os outros nenhum). ")
    st.markdown(f"- A média desse índice, quando usado para aferição de desigualdade \
                em campeonatos de pontos corridos, varia em cada país. No Brasil, \
                o pico foi o campeonato de 2019 ({max(gini_temporadas):.2f}), \
                campanha recorde do Flamengo; tal campanha é, por diversas \
                métricas, um ponto discrepante, a média do índice é cerca de \
                {np.mean(gini_temporadas):.2f}.")
    
    fig = px.line(x=temporadas, y=gini_temporadas,
                  title="Desigualdade na pontuação dos times", markers=True,
              labels={"x": "Temporada", "y": "Índice de Gini"})
    fig['data'][0]['line']['color'] = "#179422"
    fig.add_hline(y=np.mean(gini_temporadas), line_dash="dash", line_color="red",
                  annotation_text=f"Média: {np.mean(gini_temporadas):.2f}",
                  annotation_position="top right")
    st.plotly_chart(fig, theme=None, width='stretch')

with tab3:
    #st.write("#### Distância entre campeão e o vice")
    gap_campeao = []
    for temp in temporadas:
        pontos = df[df['CAMPEONATO'] == temp]['PONTOS'].sort_values(ascending=False).values
        gap_campeao.append(pontos[0] - pontos[1])

    fig = px.bar(
        x=temporadas, y=gap_campeao, title="Distância do campeão",
        color_discrete_sequence=["#09EDF5"],
        labels={"x": "Temporada", "y": "Pontos de diferença entre campeão e vice"})
    
    fig.add_hline(y=np.mean(gap_campeao), line_dash="dash", line_color="red",
                  annotation_text=f"Média: {np.mean(gap_campeao):.2f}",
                  annotation_position="top right")
    st.plotly_chart(fig, theme=None, width='stretch')

with tab4:
    #st.write("#### Desvio padrão dos pontos")
    desvios = [np.std(df[df['CAMPEONATO']==temp]['PONTOS']) for temp in temporadas]
    media = [np.mean(df[df['CAMPEONATO']==temp]['PONTOS']) for temp in temporadas]
    coef_var = [d/m for d,m in zip(desvios, media)]

    fig = px.line(x=temporadas, y=desvios,
                  title="Desvio Padrão por Temporada", markers=True,
                  labels={"x": "Temporada", "y": "Desvio Padrão"})
    #fig.add_scatter(x=temporadas, y=coef_var, mode='lines+markers', name="Coeficiente de variação")
    st.plotly_chart(fig, theme=None, width='stretch')

with tab5:
    #st.write("#### Boxplot de Pontos por Temporada")
    fig = px.box(df, x = "CAMPEONATO", y = "PONTOS", color = "CAMPEONATO",
              title = "Desempenho por temporada",
              labels = {"CAMPEONATO": "Temporada",
                        "PONTOS": "Pontos"})

    fig.update_traces(line = {'width':.7})
    st.plotly_chart(fig, theme = None, width = 'stretch')

with tab6:
    #st.write("#### Índice combinado de competitividade")
    st.markdown("O índice combinado de competitividade é uma métrica composta \
                que integra várias medidas para avaliar a competitividade geral \
                de cada temporada. Ele normaliza e combina o desvio padrão, a \
                distância do campeão e o índice de Gini para fornecer uma visão \
                holística da competitividade em cada temporada. Quanto mais \
                próximo de 1, mais competitivo é o campeonato; quanto mais \
                próximo de 0, menos competitivo.")
    # Normaliza métricas
    metrics = np.array([desvios, gap_campeao, gini_temporadas]).T
    metrics_scaled = (metrics - metrics.min(axis=0)) / (metrics.max(axis=0) - metrics.min(axis=0))

    # Competitividade = 1 - média das métricas de desigualdade
    competitividade = 1 - np.mean(metrics_scaled, axis=1)

    fig = px.line(x=temporadas, y=competitividade, markers=True,
                  title="Índice Combinado de Competitividade",
                  labels={"x": "Temporada", "y": "Valor"})
    fig['data'][0]['line']['color'] = "#F5AA09"
    st.plotly_chart(fig, theme=None, width='stretch')
