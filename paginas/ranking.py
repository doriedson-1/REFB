import pandas as pd
import streamlit as st
import plotly.express as px
import random
from recursos import Bases

# Instância
bases = Bases()

###############################################################################
# Lê o arquivo
df_jogos = bases.ler('pontos_corridos.xlsx', 'br')

# Correções ortográficas
df_jogos['time_mandante']= bases.grafia(df_jogos['time_mandante'])
df_jogos['time_visitante'] = bases.grafia(df_jogos['time_visitante'])

# # 2. Criar o widget de seleção de datas (slider ou input de data)
# # O st.date_input é mais intuitivo para selecionar um range de datas específico.
data_minima = df_jogos['data'].min()
data_maxima = df_jogos['data'].max()
data_inicial_filtro, data_final_filtro = st.date_input(
     label = "Selecione o período para a pontuação:",
     value = [data_minima, data_maxima], # Valor padrão é o campeonato todo
     min_value = data_minima,
     max_value = data_maxima,
     format = 'DD/MM/YYYY'
)
 
# 3. Filtrar os dados com base na seleção do usuário
df_filtrado = df_jogos[
     (df_jogos['data'] >= pd.to_datetime(data_inicial_filtro)) & 
     (df_jogos['data'] <= pd.to_datetime(data_final_filtro))
]

def calcular_classificacao_completa(df_filtrado):
    # 1. Processar dados como Mandante
    mandantes = df_filtrado.groupby('time_mandante').agg(
        JOGOS=('time_mandante', 'count'),
        VITORIAS=('gols_mandante', lambda x: (x > df_filtrado.loc[x.index, 'gols_visitante']).sum()),
        EMPATES=('gols_mandante', lambda x: (x == df_filtrado.loc[x.index, 'gols_visitante']).sum()),
        DERROTAS=('gols_mandante', lambda x: (x < df_filtrado.loc[x.index, 'gols_visitante']).sum()),
        GOLS_PRO=('gols_mandante', 'sum'),
        GOLS_CONTRA=('gols_visitante', 'sum')
    ).rename_axis('Time')

    # 2. Processar dados como Visitante
    visitantes = df_filtrado.groupby('time_visitante').agg(
        JOGOS=('time_visitante', 'count'),
        VITORIAS=('gols_visitante', lambda x: (x > df_filtrado.loc[x.index, 'gols_mandante']).sum()),
        EMPATES=('gols_visitante', lambda x: (x == df_filtrado.loc[x.index, 'gols_mandante']).sum()),
        DERROTAS=('gols_visitante', lambda x: (x < df_filtrado.loc[x.index, 'gols_mandante']).sum()),
        GOLS_PRO=('gols_visitante', 'sum'),
        GOLS_CONTRA=('gols_mandante', 'sum')
    ).rename_axis('Time')

    # 3. Consolidar as duas tabelas (Soma mandante + Visitante)
    # fill_value evita erro se um time não jogou no período como mandante ou visitante
    tabela = mandantes.add(visitantes, fill_value=0).astype(int)

    # 4. Calcular colunas derivadas (Pontos, Saldo e Aproveitamento)
    tabela['PONTOS'] = (tabela['VITORIAS'] * 3) + tabela['EMPATES']
    tabela['SALDO_GOLS'] = tabela['GOLS_PRO'] - tabela['GOLS_CONTRA']
    
    # Cálculo de aproveitamento com proteção contra divisão por zero
    tabela['APROVEITAMENTO'] = (tabela['PONTOS'] / (tabela['JOGOS'] * 3) * 100).round(1).fillna(0)

    # 5. Ordenação oficial (Pontos > Vitórias > Saldo > Gols Pro)
    tabela = tabela.sort_values(
        by=['PONTOS', 'VITORIAS', 'SALDO_GOLS', 'GOLS_PRO'], 
        ascending=False
    ).reset_index()

    return tabela


# --- No corpo do Streamlit ---
if not df_filtrado.empty:
    classificacao = calcular_classificacao_completa(df_filtrado)
    
    st.subheader("Tabela acumulada Brasileirão pontos corridos")
    st.dataframe(
        classificacao, 
        column_config={
            "APROVEITAMENTO": st.column_config.NumberColumn(format="%.1f%%")
        },
        hide_index=True
    )
else:
    st.warning("Nenhum jogo encontrado no período selecionado.")

###############################################################################
st.subheader("Série temporal")

arquivo = bases.ler('TabelaFinal.xlsx', 'br')
arquivo['TIME'] = bases.grafia(arquivo['TIME'])

pontos_time = arquivo.groupby(['CAMPEONATO', 'TIME'])['PONTOS'].sum().reset_index()
todos_times = bases.descritivas()

def shuffle_colors():
    # 1. Generate 50 distinct colors from a continuous scale (e.g., 'turbo', 'rainbow', or 'viridis')
    # This prevents the "out of index" error by creating a spectrum specifically for 50 points
    ncores = px.colors.sample_colorscale(
        "turbo", [i/(len(todos_times)-1) for i in range(len(todos_times))]
        )

    # 2. Shuffle the generated colors so they aren't in gradient order
    random.shuffle(ncores)
    
    # 3. Map to session state
    st.session_state.color_map = {
        str(name).strip(): color for name, color in zip(todos_times, ncores)
        #team: new_palette[i] for i, team in enumerate(times)
        }

# Initialize state
if 'color_map' not in st.session_state:
    shuffle_colors()

# 4. User interface: Shuffle Button
st.button("🔀 Mudar cores", on_click = shuffle_colors)

fig = px.line(pontos_time, x = "CAMPEONATO", y = "PONTOS", color = "TIME",
              title = "Desempenho por time", markers = True,              
              labels = {"Pontos": "Total Points",
                        "Temporada": "Temp"},
              category_orders = {'TIME':todos_times},
              color_discrete_map = st.session_state.color_map)

fig.update_traces(line = {'width':.7})

st.plotly_chart(fig, theme = None, use_container_width=True)

    # Display in Streamlit
    #return pontos_time, fig

#st.sidebar.header('Filtros')
#selecionar = st.sidebar.multiselect('Selecione', options = todos_times, default= todos_times)

#fig.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="Title Contender")
#fig.add_hline(y = pontos_time['PONTOS'].mean(), line_dash="dot", line_color="gray", annotation_text="Média")
