# Tabelas brasileirão 1971-2002
import pandas as pd
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
from recursos import Bases

bases = Bases()

def render_html_css(html_path, css_path, height=600, scrolling=True):
    """
    ----------
    html_path : TYPE
        DESCRIPTION.
    css_path : TYPE
        DESCRIPTION.
    height : TYPE, optional
        DESCRIPTION. The default is 600.
    scrolling : TYPE, optional
        DESCRIPTION. The default is True.

    Raises
    ------
    FileNotFoundError
        DESCRIPTION.

    Returns
    -------
    None.

    """
    html_path = Path(html_path)
    css_path = Path(css_path)

    if not html_path.exists():
        raise FileNotFoundError(f"HTML não encontrado: {html_path}")

    if not css_path.exists():
        raise FileNotFoundError(f"CSS não encontrado: {css_path}")

    html = html_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")

    # Remove <link rel="stylesheet"> se existir
    html = html.replace('<link rel="stylesheet" href="style.css">', '')

    full_html = f"""
    <style>
    {css}
    </style>
    {html}
    """
    
    components.html(
        full_html,
        height=height,
        scrolling=scrolling
    )

def render_tabela_classificacao(df: pd.DataFrame):
    st.subheader("Tabela (classificatória)")

    # --- 1. Tratamento Inicial ---
    df['TIME'] = bases.grafia(df['TIME'])
    
    # --- 2. FILTRO TEMPORADA ---
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
    
    # --- 3.1. Ordenação padrão ---
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


st.subheader('Primeira fase')

dados = bases.ler('2002fi.csv', 'br')
df = pd.DataFrame(dados)
render_tabela_classificacao(df)

st.divide()

st.subheader('Fase final')
render_html_css(
    html_path = st.secrets.atalhos.bd_cb_ff + "2002CB.html",
    css_path= st.secrets.atalhos.css,
    height=700)
