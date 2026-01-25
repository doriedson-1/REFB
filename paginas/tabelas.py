import streamlit as st
import pandas as pd
from recursos import Bases

bases = Bases()

def render_tabela_classificacao(df: pd.DataFrame):
    st.subheader("🏆 Tabela de classificação")

    # --- 1. Tratamento Inicial ---
    # Garante que nomes de colunas não tenham espaços extras e estejam padronizados
    # Se suas colunas já estão certas, isso não atrapalha
    df.columns = [c.strip() for c in df.columns]

    # --- 2. Filtro de Temporada ---
    if 'CAMPEONATO' in df.columns:
        # Ordena as temporadas (ex: 2024, 2023...)
        temporadas = sorted(df['CAMPEONATO'].unique(), reverse=True)
        
        col_filtro, _ = st.columns([1, 3])
        with col_filtro:
            selecao_temp = st.selectbox("Selecione a Temporada:", temporadas)
        
        # Filtra o DataFrame
        df_show = df[df['CAMPEONATO'] == selecao_temp].copy()
    else:
        st.error("Coluna 'CAMPEONATO' não encontrada.")
        return

    # --- 3. Ordenação Padrão de Futebol ---
    # Critérios: Pontos (desc), Vitórias (desc), Saldo (desc), Gols Pró (desc)
    cols_sort = ['PONTOS', 'VITORIAS', 'SALDO_GOLS', 'GOLS_PRO']
    cols_existentes_sort = [c for c in cols_sort if c in df_show.columns]
    
    if cols_existentes_sort:
        df_show = df_show.sort_values(by=cols_existentes_sort, ascending=False)

    # --- 4. Ajuste de Índice (Rank) ---
    # Reseta o index para virar 1º, 2º, 3º...
    df_show = df_show.reset_index(drop=True)
    df_show.index = df_show.index + 1

    # --- 5. Seleção e Renomeação de Colunas para Exibição ---
    # Definimos quais colunas mostrar e a ordem
    cols_display = [
        'TIME', 'PONTOS', 'JOGOs', 'VITORIAS', 'EMPATES', 'DERROTAS', 
        'GOLS_PRO', 'GOLS_CONTRA', 'SALDO_GOLS', 'APROVEITAMENTO'
    ]
    # Filtra apenas as que existem no seu CSV
    cols_finais = [c for c in cols_display if c in df_show.columns]

    # --- 6. Exibição com Column Config (A mágica visual) ---
    st.dataframe(
        df_show[cols_finais],
        use_container_width=True,
        column_config={
            "TIME": st.column_config.TextColumn(
                "Clube",
                width="medium"
            ),
            "PONTOS": st.column_config.NumberColumn(
                "Pts",
                format="%d", # Inteiro
            ),
            "JOGOS": st.column_config.NumberColumn("Jogos"),
            "VITORIAS": st.column_config.NumberColumn("Vitórias"),
            "EMPATES": st.column_config.NumberColumn("Empates"),
            "DERROTAS": st.column_config.NumberColumn("Derrotas"),
            "GOLS_PRO": st.column_config.NumberColumn("Gols pró"),
            "GOLS_CONTRA": st.column_config.NumberColumn("Gols contra"),
            "SALDO_GOLS": st.column_config.NumberColumn(
                "SG",
                format="%d"
            ),
            "APROVEITAMENTO": st.column_config.ProgressColumn(
                "Aprov. %",
                format="%.1f%%", # Ex: 55.4%
                min_value=0,
                max_value=100,   # Assumindo que seus dados estão em escala 0-100
            ),
        }
    )

dados = bases.ler('TabelaFinal.xlsx', 'br')
df = pd.DataFrame(dados)
render_tabela_classificacao(df)