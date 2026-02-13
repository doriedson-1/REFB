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


st.divider()
st.subheader('Primeira fase')

dados = bases.ler('2002fi.csv', 'br')

# Ordena as temporadas
temporadas = sorted(dados['campeonato'].unique(), reverse=True)
    
col_filtro, _ = st.columns([1, 3])
with col_filtro:
    selecao_temp = st.selectbox("Selecione a temporada:", temporadas)
    
    # Filtra o DataFrame
    df_show = dados[dados['campeonato'] == selecao_temp].copy()

tab = bases.classifica(dados, selecao_temp)
st.dataframe(tab)

st.divider()

st.subheader('Fase final')
render_html_css(
    html_path = st.secrets.atalhos.bd_cb_ff + "2002CB.html",
    css_path= st.secrets.atalhos.css,
    height=700)
