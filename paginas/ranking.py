# Página do ranking geral do campeonato brasileiro de pontos corridos (2003-2025)
import pandas as pd
import streamlit as st
import plotly.express as px
import random
from recursos import Bases

# Instância
bases = Bases()

@st.cache_data
def calcular_classificacao_completa(df_filtrado):
    """
    Calcula a classificação dado um dataframe de partidas.
    """
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

    # 4. Calcular colunas derivadas
    tabela['PONTOS'] = (tabela['VITORIAS'] * 3) + tabela['EMPATES']
    tabela['SALDO_GOLS'] = tabela['GOLS_PRO'] - tabela['GOLS_CONTRA']
    
    # --- ALTERAÇÃO MANUAL tapetao ---
    ajustes_pontos = {
        'Barueri': -3,
        'Corinthians': 2,
        'Flamengo': -4,
        'Fluminense': 2,
        'Internacional': 2,
        'Juventude': 3,
        'Paysandu SC': -8,
        'Ponte Preta': - 4 + 3,
        'Portuguesa': - 4,
        'São Caetano':3 - 24        
    }
    ajustes_sg = {
        'Atlético-MG': -3,
        'Chapecoense': -3}

    for time, ajuste in ajustes_pontos.items():
        if time in tabela.index:
            tabela.at[time, 'PONTOS'] += ajuste
    for time, ajuste in ajustes_sg.items():
        if time in tabela.index:
            tabela.at[time, 'SALDO_GOLS'] += ajuste

    # 5. Ordenação oficial (Pontos > Vitórias > Saldo > Gols Pro)
    tabela = tabela.sort_values(
        by=['PONTOS', 'VITORIAS', 'SALDO_GOLS', 'GOLS_PRO'], 
        ascending=False
    ).reset_index()
     
    tabela['APROVEITAMENTO'] = (tabela['PONTOS'] / (tabela['JOGOS'] * 3) * 100).round(1).fillna(0)
    
    # 6. Participações
    df1 = df_filtrado.groupby(['ano_campeonato', 'time_mandante',]).size().to_frame('size').reset_index()
    part = df1['time_mandante'].value_counts().to_frame(
        'TEMPORADAS').reset_index().rename(columns={'time_mandante':'Time'})
    tabela = tabela.merge(part, how = 'left', on = 'Time')
    
    
    # Imagens
    # Passo A: Obter o código
    tabela['codigo_temp'] = tabela['Time'].apply(bases.codigo_clube)
    # Passo B: Montar a URL completa
    base_url = "https://tmssl.akamaized.net//images/wappen/head/"
    tabela['ESCUDO'] = tabela['codigo_temp'].apply(lambda x: f"{base_url}{x}")

    return tabela


def shuffle_colors():
    # 1. Geração de cores escala contínua
    # (https://plotly.com/python/colorscales/#continuous-color-with-plotly-express)
    ncores = px.colors.sample_colorscale(
        'jet', [i/(len(todos_times)-1) for i in range(len(todos_times))]
        )

    # 2. Mistura ordem das cores
    random.shuffle(ncores)
    
    # 3. Mapeamento p/ estado inicial
    st.session_state.color_map = {
        str(name).strip(): color for name, color in zip(todos_times, ncores)
        }

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
     label = "Selecione um recorte de tempo para a tabela:",
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

# --- No corpo do Streamlit ---
if not df_filtrado.empty:
    classificacao = calcular_classificacao_completa(df_filtrado)
    
    # Mudança de ordem
    classificacao = classificacao.iloc[:, [12,0,1,7,2,3,4,5,6,8,9,10]]
    
    st.subheader("Tabela acumulada Brasileirão (2003-2025)")
    st.dataframe(
        classificacao, 
        column_config = {
            # Configuração da Imagem
            "ESCUDO": st.column_config.ImageColumn("", width="small"),
            "APROVEITAMENTO": st.column_config.NumberColumn(format="%.2f%%")
        },
        hide_index=True
    )
else:
    st.warning("Nenhum jogo encontrado no período selecionado.")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
with st.expander('Evolução dos pontos corridos (vídeo)'):
    bases.video('CB_pc.mp4')

###############################################################################
st.subheader("Série temporal")

arquivo = bases.ler('TabelaFinal.xlsx', 'br')
arquivo['TIME'] = bases.grafia(arquivo['TIME'])

pontos_time = arquivo.groupby(['CAMPEONATO', 'TIME'])['PONTOS'].sum().reset_index()
todos_times = bases.descritivas()


# Estado inicial
if 'color_map' not in st.session_state:
    shuffle_colors()

# UI: Botão
st.button("🔀 Mudar cores", on_click = shuffle_colors)

fig = px.line(pontos_time, x = "CAMPEONATO", y = "PONTOS", color = "TIME",
              title = "Desempenho por time",
              markers = True,              
              labels = {"Pontos": "Total Points",
                        "Temporada": "Temp"},
              category_orders = {'TIME':todos_times},
              color_discrete_map = st.session_state.color_map)

fig.update_traces(line = {'width':.7})

st.plotly_chart(fig, theme = None, width = 'stretch')

st.markdown("- Nas temporadas de 2003 e 2004 o campeonato foi disputado com 24 clubes;")
st.markdown("- Na temporada de 2005 o campeonato foi disputado com 22 clubes;")
st.markdown("- Desde  2006 o campeonato (série A) é disputado com\
            20 clubes e os quatro piores colocados são rebaixados\
            para a série B;")
st.markdown("- O campeonato brasileiro de 2020 teve início em \
            08/08/2020 e fim em 25/02/2021, devido à pandemia de COVID-19;")
st.markdown("- O campeonato brasileiro de 2021 teve início em 29/05/2021 e fim em\
            09/12/2021.")


#st.sidebar.header('Filtros')
#selecionar = st.sidebar.multiselect('Selecione', options = todos_times, default= todos_times)

#fig.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="Title Contender")
#fig.add_hline(y = pontos_time['PONTOS'].mean(), line_dash="dot", line_color="gray", annotation_text="Média")

st.markdown('---')

st.subheader('Decisões do STJD')

with st.expander('**2003**'):
    st.markdown('- Ponte Preta perdeu 4 pontos por escalar irregularmente o jogador \
        Roberto nas partidas contra Internacional e Juventude;')
    st.markdown('- Juventude ganhou 3 pontos do jogo contra a Ponte Preta;')
    st.markdown('- Internacional ganhou 2 pontos do jogo contra a Ponte Preta;')
    st.markdown('- O Paysandu perdeu 8 pontos pela escalação irregular dos jogadores\
        Júnior Amorim e Aldrovani, nos jogos contra São Caetano, Fluminense,\
        Corinthians e Ponte Preta;')
    st.markdown('- São Caetano ganhou 3 pontos dos jogos contra o Paysandu;')
    st.markdown('- Corinthians ganhou 2 pontos dos jogos contra o Paysandu;')
    st.markdown('- Fluminense ganhou 2 pontos dos jogos contra o Paysandu.')

with st.expander('**2004**'):
    st.markdown('- O São Caetano foi punido com a perda de 24 pontos\' \
        pelo STJD, pela morte do jogador Serginho. Analistas indicaram que\
        o clube teve conhecimento que o atleta tinha problemas cardíacos e\
        não poderia continuar sua carreira.')

with st.expander('**2005**'):
    st.markdown('- A CBF havia punido o Brasiliense com o jogo de estreia sem torcida,\
        a justiça comum reverteu a punição e o público viu a partida entre \
        Brasiliense e Vasco da Gama terminar empatada em 2 a 2; posteriormente,\
        a vitória foi atribuída ao Vasco da Gama (0-1);')
    st.markdown('- O esquema de manipulação de resultados conhecido como "Máfia do apito"\
        causou a anulação de onze jogos.')

with st.expander('**2010**'):
    st.markdown('- O Grêmio Prudente (posteriormente, Barueri) perdeu 3 pontos pela \
        escalação irregular do zagueiro Paulão na derrota para o Flamengo.')

with st.expander('**2013**'):
    st.markdown('- A Portuguesa de Desportos perdeu 4 pontos, foi punida por ter \
        escalado irregularmente o jogador Héverton contra o Grêmio, na última\
        rodada;')
    st.markdown('- O Flamengo perdeu 4 pontos, foi punido pela escalação irregular do\
        lateral-esquerdo André Santos na partida contra o Cruzeiro.')

with st.expander('**2016**'):
    st.markdown('- Atlético-MG e Chapecoense obtiveram WO (_walkover_) duplo em virtude do desastre\
        aéreo que vitimou a delegação da Chapecoense no dia 29 de novembro,\
        na Colômbia; foram adicionados 3 gols negativos.')
