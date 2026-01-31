# Estatísticas dos clubes
import streamlit as st
import pandas as pd
import numpy as np
from recursos import Bases

# Instância
bases = Bases()

def render_dashboard_time(df: pd.DataFrame):
    st.header("📊 Dashboard do Time")

    # --- 1. SELETOR DE TIME (O Gatilho da Performance) ---
    df['time_mandante'] = bases.grafia(df['time_mandante'])
    df['time_visitante'] = bases.grafia(df['time_visitante'])

    todos_times = sorted(pd.concat([df['time_mandante'], df['time_visitante']]).unique())
    
    c1, c2 = st.columns([1, 3])
    with c1:
        time_sel = st.selectbox("Escolha o Clube:", todos_times)
    
    # --- 2. FILTRAGEM E NORMALIZAÇÃO (Onde a mágica acontece) ---
    # Passo A: Filtra apenas jogos desse time (seja casa ou fora)
    # Isso reduz drasticamente o volume de dados a processar
    mask = (df['time_mandante'] == time_sel) | (df['time_visitante'] == time_sel)
    df_time = df[mask].copy()

    if df_time.empty:
        st.warning("Sem dados para este time.")
        return

    # Passo B: Normalização Vetorizada (Muito Rápido)
    # Criamos colunas padronizadas independentemente do mando de campo
    
    # Se o time selecionado é o mandante, o adversário é o visitante (e vice-versa)
    condicao_mandante = df_time['time_mandante'] == time_sel
    
    df_time['Adversario'] = np.where(condicao_mandante, df_time['time_visitante'],
                                     df_time['time_mandante'])
    df_time['Gols_Pro'] = np.where(condicao_mandante, df_time['gols_mandante'],
                                   df_time['gols_visitante'])
    df_time['Gols_Contra'] = np.where(condicao_mandante, df_time['gols_visitante'],
                                      df_time['gols_mandante'])
    df_time['Mando'] = np.where(condicao_mandante, 'Casa', 'Fora')
    
    # Tratamento de tipos para garantir contas certas
    df_time['Gols_Pro'] = df_time['Gols_Pro'].fillna(0).astype(int)
    df_time['Gols_Contra'] = df_time['Gols_Contra'].fillna(0).astype(int)
    df_time['Saldo'] = df_time['Gols_Pro'] - df_time['Gols_Contra']

    # --- 3. DASHBOARD DE ESTATÍSTICAS ---
    
    # Métricas de Cabeçalho
    vitorias = len(df_time[df_time['Saldo'] > 0])
    derrotas = len(df_time[df_time['Saldo'] < 0])
    empates = len(df_time[df_time['Saldo'] == 0])
    saldo_total = df_time['Saldo'].sum()
    
    with c2:
        # Exibe métricas rápidas ao lado do seletor
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Jogos", len(df_time))
        m2.metric("Vitórias", vitorias, delta=f"{saldo_total} SG")
        m3.metric("Empates", empates)
        m4.metric("Derrotas", derrotas, delta_color="inverse")

    st.divider()

    # --- 4. ANÁLISE DE GOLEADAS (Filtro Interativo) ---
    st.subheader(f"🔎 Análise de Jogos: {time_sel}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        tipo_resultado = st.radio(
            "Filtrar por resultado:",
            ["Todas", "Vitórias (Goleadas a favor)", "Derrotas (Goleadas sofridas)"],
            horizontal=True
        )
    with col_b:
        dif_min = st.slider("Diferença mínima de gols:", 1, 11, 3)

    # Lógica de Filtro Visual
    df_show = df_time.copy()
    
    if "Vitórias" in tipo_resultado:
        df_show = df_show[df_show['Saldo'] >= dif_min] # Saldo positivo >= X
        msg_vazio = f"Nenhuma vitória por {dif_min} ou mais gols."
    elif "Derrotas" in tipo_resultado:
        df_show = df_show[df_show['Saldo'] <= -dif_min] # Saldo negativo <= -X
        msg_vazio = f"Nenhuma derrota por {dif_min} ou mais gols."
    else:
        # Se for "Todas", filtra apenas pela magnitude da diferença (para qualquer lado)
        df_show = df_show[df_show['Saldo'].abs() >= dif_min]
        msg_vazio = f"Nenhum jogo com diferença de {dif_min} gols."

    # Ordenar por data mais recente
    if 'data' in df_show.columns:
        df_show['data'] = pd.to_datetime(df_show['data'])
        df_show = df_show.sort_values('data', ascending=False)

    # --- 5. TABELA FINAL ---
    if df_show.empty:
        st.info(msg_vazio)
    else:
        # Criação da coluna Placar Visual (ex: 4 x 1)
        df_show['Placar'] = df_show.apply(lambda x: f"{x['Gols_Pro']} x {x['Gols_Contra']}", axis=1)

        st.dataframe(
            df_show[['data', 'Mando', 'Adversario', 'Placar', 'Saldo']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                #"campeonato": st.column_config.TextColumn("Camp."),
                "Mando": st.column_config.TextColumn("Local"),
                "Adversario": st.column_config.TextColumn("Oponente"),
                "Placar": st.column_config.TextColumn("Placar"),
                "Saldo": st.column_config.NumberColumn("Dif.", format="%d")}
        )

df = bases.ler('pontos_corridos.xlsx', 'br')
render_dashboard_time(df)
    
  