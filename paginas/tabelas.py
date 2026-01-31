import streamlit as st
import pandas as pd
from recursos import Bases

bases = Bases()

def render_tabela_classificacao(df: pd.DataFrame):
    st.subheader("🏆 Tabela de classificação")

    # --- 1. Tratamento Inicial ---
    df['TIME'] = bases.grafia(df['TIME'])
    
    # --- 2. Filtro de Temporada ---
    if 'CAMPEONATO' in df.columns:
        # Ordena as temporadas
        temporadas = sorted(df['CAMPEONATO'].unique(), reverse=True)
        
        col_filtro, _ = st.columns([1, 3])
        with col_filtro:
            selecao_temp = st.selectbox("Selecione a temporada:", temporadas)
        
        # Filtra o DataFrame
        df_show = df[df['CAMPEONATO'] == selecao_temp].copy()
    else:
        st.error("Coluna 'CAMPEONATO' não encontrada.")
        return
    
    # Imagens
    # Passo A: Obter o código
    df_show['codigo_temp'] = df_show['TIME'].apply(bases.codigo_clube)
    
    # Passo B: Montar a URL completa
    base_url = "https://tmssl.akamaized.net//images/wappen/head/"
    df_show['ESCUDO'] = df_show['codigo_temp'].apply(lambda x: f"{base_url}{x}")

    # --- 3. Ordenação padrão ---
    cols_sort = ['PONTOS', 'VITORIAS', 'SALDO_GOLS', 'GOLS_PRO']
    cols_existentes_sort = [c for c in cols_sort if c in df_show.columns]
    
    if cols_existentes_sort:
        df_show = df_show.sort_values(by=cols_existentes_sort, ascending=False)

    # --- 4. Ajuste de índice ---
    df_show = df_show.reset_index(drop=True)
    df_show.index = df_show.index + 1

    # --- 5. Seleção de colunas ---
    cols_display = [
        'ESCUDO', 'TIME', 'PONTOS', 'JOGOS', 'VITORIAS', 'EMPATES', 'DERROTAS', 
        'GOLS_PRO', 'GOLS_CONTRA', 'SALDO_GOLS', 'APROVEITAMENTO'
    ]
    # Filtro
    cols_finais = [c for c in cols_display if c in df_show.columns]

    # --- 6. Exibição ---
    st.dataframe(
        df_show[cols_finais],
        width='stretch',
        column_config={
            # Configuração da Imagem
            "ESCUDO": st.column_config.ImageColumn("", width="small"), # Opções: "small", "medium", "large
            "TIME": st.column_config.TextColumn("Clube", width="medium"),
            "PONTOS": st.column_config.NumberColumn("Pontos", format = "%d",),
            "JOGOS": st.column_config.NumberColumn("Jogos"),
            "VITORIAS": st.column_config.NumberColumn("Vitórias"),
            "EMPATES": st.column_config.NumberColumn("Empates"),
            "DERROTAS": st.column_config.NumberColumn("Derrotas"),
            "GOLS_PRO": st.column_config.NumberColumn("Gols pró"),
            "GOLS_CONTRA": st.column_config.NumberColumn("Gols contra"),
            "SALDO_GOLS": st.column_config.NumberColumn("Saldo",format = "%d"),
            "APROVEITAMENTO": st.column_config.ProgressColumn(
                "Aprov. %", format="%.1f%%", min_value=0, max_value=100,),
        }
    )

dados = bases.ler('TabelaFinal.xlsx', 'br')
df = pd.DataFrame(dados)
render_tabela_classificacao(df)