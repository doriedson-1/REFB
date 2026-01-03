# Mano a mano dos times
import pandas as pd
import streamlit as st
import numpy as np
import time
from recursos import Bases

# Instância
bases = Bases()

def render_confrontos_detalhados(df: pd.DataFrame):
    """
    Renderiza a seção de análise de confrontos (mano a mano)
    baseado em estrutura Mandante/Visitante e Gols.
    """
    st.divider()
    st.subheader("⚔️ Análise de Confrontos Diretos")

    # --- 1. Filtros de Seleção ---
    c1, c2, c3 = st.columns([2, 2, 2])
    
    # Lista única de times e campeonatos
    all_teams = bases.descritivas()
    all_champs = sorted(df['campeonato'].unique())

    with c1:
        # Filtro de Campeonato (Opcional)
        campeonato = st.selectbox(
            "Filtrar Campeonato:", 
            ["Todos"] + all_champs
        )

    with c2:
        # Time A (Tenta usar o pré-selecionado se existir e for válido)
        idx_padrao = 0
        time_a = st.selectbox("Time:", all_teams, index = idx_padrao)

    with c3:
        # Time B (Remove o Time A da lista)
        oponents = [t for t in all_teams if t != time_a]
        time_b = st.selectbox("Adversário:", oponents)

    # --- 2. Processamento dos Dados ---
    # Passo A: Filtrar Times (A vs B ou B vs A)
    mask_teams = (
        ((df['time_mandante'] == time_a) & (df['time_visitante'] == time_b)) |
        ((df['time_mandante'] == time_b) & (df['time_visitante'] == time_a))
    )
    time.sleep(5)
    # Passo B: Filtrar Campeonato
    if campeonato != "Todos":
        mask_final = mask_teams & (df['campeonato'] == campeonato)
    else:
        mask_final = mask_teams

    df_filtered = df[mask_final].copy()

    # --- 3. Exibição ---
    if df_filtered.empty:
        st.info(f"Não foram encontrados jogos entre **{time_a}** e **{time_b}** com os filtros atuais.")
        return

    # Ordenar por data (assumindo que existe uma coluna 'data' ou 'ano')
    # Se não tiver 'data', substitua por 'ano' ou índice
    if 'data' in df_filtered.columns:
        df_filtered = df_filtered.sort_values('data', ascending=False)

    # --- 4. Tabela de Jogos ---
    st.markdown("### 📜 Histórico de Partidas")

    # Função de estilo para colorir linhas baseado no resultado do Time A
    def style_row(row):
        # Lógica para determinar resultado do ponto de vista do Time A
        gols_a = row['gols_mandante'] if row['time_mandante'] == time_a else row['gols_visitante']
        gols_b = row['gols_visitante'] if row['time_mandante'] == time_a else row['gols_mandante']
        
        if gols_a > gols_b:
            return ['background-color: #d4edda; color: #155724'] * len(row) # Verde (Vitória)
        elif gols_a < gols_b:
            return ['background-color: #f8d7da; color: #721c24'] * len(row) # Vermelho (Derrota)
        else:
            return ['background-color: #fff3cd; color: #856404'] * len(row) # Amarelo (Empate)

    # Selecionar colunas relevantes para exibição
    cols_display = ['data', 'campeonato', 'time_mandante',
                    'gols_mandante', 'gols_visitante', 'time_visitante']
    # Ajuste as colunas conforme existam no seu DF
    cols_final = [c for c in cols_display if c in df_filtered.columns]

    st.dataframe(
        df_filtered[cols_final].style.apply(style_row, axis=1),
        use_container_width=True,
        hide_index=True
    )

    _mostrar_resumo_estatistico(df_filtered, time_a, time_b)

def _mostrar_resumo_estatistico(df: pd.DataFrame, time_a: str, time_b: str):
    """
    Calcula e exibe as estatísticas agregadas.
    Função auxiliar privada para manter o código limpo.
    """
    # Vetorização para cálculo rápido
    # Condições onde A é mandante
    is_a_home = df['time_mandante'] == time_a
    
    # Gols marcados por A e B
    gols_a = np.where(is_a_home, df['gols_mandante'], df['gols_visitante'])
    gols_b = np.where(is_a_home, df['gols_visitante'], df['gols_mandante'])

    total_jogos = len(df)
    vitorias = np.sum(gols_a > gols_b)
    derrotas = np.sum(gols_a < gols_b)
    empates  = np.sum(gols_a == gols_b)
    
    st.markdown("---")
    st.subheader("📊 Resumo")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Jogos", total_jogos)
    with col2:
        st.metric(f"Vitórias {time_a}", int(vitorias),
                  delta=f"{(vitorias/total_jogos)*100:.1f}%" if total_jogos else None)
    with col3:
        st.metric("Empates", int(empates))
    with col4:
        st.metric(f"Vitórias {time_b}", int(derrotas), delta_color="inverse")


df = bases.ler('pontos_corridos.xlsx', 'br')
df['campeonato'] = 'Brasileiro'

# Correções ortográficas
df['time_mandante']= bases.grafia(df['time_mandante'])
df['time_visitante'] = bases.grafia(df['time_visitante'])

st.write('No momento só há duelos do campeonato brasileiro (desde 2003)')

render_confrontos_detalhados(df)