import pandas as pd
import streamlit as st
from recursos import Bases

# Instância
bases = Bases()

# Lê o arquivo
df_jogos = bases.ler('pontos_corridos.xlsx', 'br')

# Correções ortográficas
df_jogos['time_mandante']= bases.grafia(df_jogos['time_mandante'])
df_jogos['time_visitante'] = bases.grafia(df_jogos['time_visitante'])

data_minima = df_jogos['data'].min()
data_maxima = df_jogos['data'].max()
 
# # 2. Criar o widget de seleção de datas (slider ou input de data)
# # O st.date_input é mais intuitivo para selecionar um range de datas específico.
data_inicial_filtro, data_final_filtro = st.date_input(
     label = "Selecione o período para a pontuação:",
     value = [data_minima, data_maxima], # Valor padrão é o campeonato todo
     min_value = data_minima,
     max_value = data_maxima,
     format = 'DD/MM/YYYY'     
)
 
# # 3. Filtrar os dados com base na seleção do usuário
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
    # pre_fill=0 evita erro se um time não jogou no período como mandante ou visitante
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

# =============================================================================
# # 1. Encontrar o intervalo completo de datas dos jogos
# data_minima = df_jogos['data'].min()
# data_maxima = df_jogos['data'].max()
# 
# # 2. Criar o widget de seleção de datas (slider ou input de data)
# # O st.date_input é mais intuitivo para selecionar um range de datas específico.
# data_inicial_filtro, data_final_filtro = st.date_input(
#     label="Selecione o período para a pontuação:",
#     value=[data_minima, data_maxima], # Valor padrão é o campeonato todo
#     min_value=data_minima,
#     max_value=data_maxima
# )
# 
# # 3. Filtrar os dados com base na seleção do usuário
# df_filtrado = df_jogos[
#     (df_jogos['data'] >= pd.to_datetime(data_inicial_filtro)) & 
#     (df_jogos['data'] <= pd.to_datetime(data_final_filtro))
# ]
# 
# # --- Lógica para calcular a pontuação (usando apenas df_filtrado) ---
# 
# def calcular_tabela(df):
#     # Implementação simplificada de cálculo de pontos
#     times = set(df['time_mandante']).union(set(df['time_visitante']))
#     pontuacao = {time: 0 for time in times}
# 
#     for index, row in df.iterrows():
#         if row['gols_mandante'] > row['gols_visitante']:
#             pontuacao[row['time_mandante']] += 3
#         elif row['gols_mandante'] < row['gols_visitante']:
#             pontuacao[row['time_visitante']] += 3
#         else:
#             pontuacao[row['time_mandante']] += 1
#             pontuacao[row['time_visitante']] += 1
#             
#     tabela_final = pd.DataFrame(list(pontuacao.items()), columns=['Time', 'Pontos'])
#     tabela_final = tabela_final.sort_values(by='Pontos', ascending=False)
#     return tabela_final
# 
# tabela_final = calcular_tabela(df_filtrado)
# 
# # 4. Exibir o resultado no Streamlit
# st.subheader("Classificação do Período Selecionado")
# st.dataframe(tabela_final, hide_index=True)
# st.caption(f"Exibindo jogos de {data_inicial_filtro} até {data_final_filtro}")
# =============================================================================

# Adiciona as colunas de pontos
#bases.pontuar(df, gol_m = 'gols_mandante', gol_v = 'gols_visitante')

#df2 = df[(df['ano_campeonato'] > 2005) ]

#tabela = bases.classifica(df2)

#st.subheader('Ranking acumalado dos pontos corridos (2003 - atual)')
#st.slider('Ano do campeonato', 2005, 2023, (2005, 2023))
