# Goleadas de cada time
import streamlit as st
import pandas as pd
import numpy as np
from recursos import Bases

bases = Bases()

# --- 1. FUNÇÃO DE PREPARAÇÃO DOS DADOS ---
# Transformamos a base "Jogo" em base "Time-Atuação" para facilitar filtros
def preparar_base_times(df):
    
    df['time_mandante'] = bases.grafia(df['time_mandante'])
    df['time_visitante'] = bases.grafia(df['time_visitante'])
    
    # Perspectiva do Mandante
    df_mand = df[['id_jogo', 'data', 'ano_campeonato', 'time_mandante', 'time_visitante', 'gols_mandante', 'gols_visitante']].copy()
    df_mand.columns = ['id_jogo', 'data', 'ano', 'time', 'oponente', 'gols_pro', 'gols_contra']
    df_mand['mando'] = 'Casa'

    # Perspectiva do Visitante
    df_vis = df[['id_jogo', 'data', 'ano_campeonato', 'time_visitante', 'time_mandante', 'gols_visitante', 'gols_mandante']].copy()
    df_vis.columns = ['id_jogo', 'data', 'ano', 'time', 'oponente', 'gols_pro', 'gols_contra']
    df_vis['mando'] = 'Fora'
    
    # Unifica
    df_final = pd.concat([df_mand, df_vis], ignore_index=True)
    
    # Cálculos
    df_final['saldo'] = df_final['gols_pro'] - df_final['gols_contra']
    
    # Define status do jogo
    conditions = [
        (df_final['saldo'] > 0),
        (df_final['saldo'] < 0),
        (df_final['saldo'] == 0)
    ]
    choices = ['Vitoria', 'Derrota', 'Empate']
    df_final['resultado'] = np.select(conditions, choices, default='Outro')
    
    return df_final

def render_estatisticas_avancadas(df_original: pd.DataFrame):
    st.subheader("📊 Estatísticas e Goleadas")

    # Prepara os dados (Cachear isso seria ideal em produção)
    df_times = preparar_base_times(df_original)
    
    # Abas para separar contextos
    tab1, tab2 = st.tabs(["🌪️ Raio-X de Goleadas", "⚖️ Comparador de Times"])

    # --- ABA 1: ANÁLISE DE GOLEADAS ---
    with tab1:
        st.caption("Filtre jogos com grandes diferenças de placar.")
        
        # Filtros no topo
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            # Slider define o que é goleada (ex: >= 3 gols de diferença)
            criterio_gols = st.slider("Diferença mínima de gols:", 2, 7, 3)
        with c2:
            tipo_filtro = st.radio("Perspectiva:", ["Goleadas aplicadas",
                                                    "Goleadas sofridas"])
        with c3:
            anos = sorted(df_times['ano'].unique(), reverse=True)
            ano_sel = st.selectbox("Temporada:", ["Todas"] + list(anos))
        with c4:
            times = sorted(df_times['time'].unique())
            time_sel = st.selectbox("Clube:", ["Todos"] + list(times))

        # Aplicação dos Filtros
        # 1. Filtra pelo saldo (positivo se aplicou, negativo se sofreu)
        if "aplicadas" in tipo_filtro:
            mask = df_times['saldo'] >= criterio_gols
            #cor_metric = "normal" # Verde/Padrão
            #label_col = "Vitórias por Goleada"
        else:
            mask = df_times['saldo'] <= -criterio_gols
            #cor_metric = "inverse" # Vermelho
            #label_col = "Derrotas por Goleada"

        if ano_sel != "Todas":
            mask = mask & (df_times['ano'] == ano_sel)
            
        if time_sel != "Todos":
                mask = mask & (df_times['time'] == time_sel)

        df_goleadas = df_times[mask].copy()

        # Visualização 1: Ranking (Gráfico)
        if not df_goleadas.empty:
            ranking = df_goleadas['time'].value_counts().head(20)
            
            st.subheader(f"Ranking - {tipo_filtro}")
            st.bar_chart(ranking, color="#ff4b4b" if "Sofreu" in tipo_filtro else "#00cc96")

            # Visualização 2: Tabela Detalhada
            st.subheader("Lista de Jogos")
            
            # Formata Placar para exibição
            df_goleadas['Placar'] = df_goleadas.apply(
                lambda x: f"{int(x['gols_pro'])} x {int(x['gols_contra'])}", axis=1
            )
            
            # Configuração visual da tabela
            st.dataframe(
                df_goleadas[['data', 'time', 'Placar', 'oponente', 'saldo', 'ano']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                    "time": st.column_config.TextColumn("Time analisado"),
                    "oponente": st.column_config.TextColumn("Adversário"),
                    "saldo": st.column_config.NumberColumn("Diferença de gols"),
                    "ano": st.column_config.TextColumn("Temp."),
                }
            )
        else:
            st.info("Nenhum jogo encontrado com estes critérios.")

    # --- ABA 2: COMPARADOR (HEAD-TO-HEAD) ---
    with tab2:
        col_a, col_b = st.columns(2)
        times_disponiveis = sorted(df_times['time'].unique())
        
        with col_a:
            time_1 = st.selectbox("Time A", times_disponiveis, index=0)
        with col_b:
            # Tenta pegar o segundo time da lista para não ser igual ao primeiro
            idx_2 = 1 if len(times_disponiveis) > 1 else 0
            time_2 = st.selectbox("Time B", times_disponiveis, index=idx_2)

        if time_1 == time_2:
            st.warning("Selecione times diferentes.")
        else:
            # Filtra jogos SOMENTE entre esses dois
            # A lógica aqui busca na base original onde (Mandante=A e Visitante=B)
            # OU (Mandante=B e Visitante=A)
            mask_confronto = (
                ((df_original['time_mandante'] == time_1) & 
                 (df_original['time_visitante'] == time_2)) |
                ((df_original['time_mandante'] == time_2) & 
                 (df_original['time_visitante'] == time_1))
            )
            df_vs = df_original[mask_confronto].copy()
            
            if df_vs.empty:
                st.info("Nunca se enfrentaram na base de dados.")
            else:
                # Cálculos de Métricas
                vitorias_t1 = len(df_vs[
                    ((df_vs['time_mandante'] == time_1) & 
                     (df_vs['gols_mandante'] > df_vs['gols_visitante'])) |
                    ((df_vs['time_visitante'] == time_1) & 
                     (df_vs['gols_visitante'] > df_vs['gols_mandante']))
                ])
                
                vitorias_t2 = len(df_vs[
                    ((df_vs['time_mandante'] == time_2) & 
                     (df_vs['gols_mandante'] > df_vs['gols_visitante'])) |
                    ((df_vs['time_visitante'] == time_2) & 
                     (df_vs['gols_visitante'] > df_vs['gols_mandante']))
                ])
                
                empates = len(df_vs) - vitorias_t1 - vitorias_t2
                
                # Exibição dos Cards
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric(f"Vitórias {time_1}", vitorias_t1,
                          delta=vitorias_t1-vitorias_t2)
                m2.metric("Empates", empates)
                m3.metric(f"Vitórias {time_2}", vitorias_t2,
                          delta=vitorias_t2-vitorias_t1, delta_color="inverse")
                
                # Goleadas no Confronto
                st.subheader("Maiores Goleadas do Confronto")
                
                # Adiciona coluna de diferença absoluta
                df_vs['dif'] = abs(df_vs['gols_mandante'] - df_vs['gols_visitante'])
                df_vs = df_vs.sort_values('dif', ascending=False).head(5)
                
                # Formata data para string
                if 'data' in df_vs.columns:
                     df_vs['data'] = pd.to_datetime(df_vs['data'])

                st.dataframe(
                    df_vs[['data', 'time_mandante', 'gols_mandante',
                           'gols_visitante', 'time_visitante']],
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                        "time_mandante": st.column_config.TextColumn("Mandante"),
                        "time_visitante": st.column_config.TextColumn("Visitante"),
                        "gols_mandante": st.column_config.NumberColumn("Gols", format="%d"),
                        "gols_visitante": st.column_config.NumberColumn("Gols", format="%d")
                    }
                )


df = bases.ler('pontos_corridos.xlsx', 'br')
df['campeonato'] = 'Brasileiro'
render_estatisticas_avancadas(df)