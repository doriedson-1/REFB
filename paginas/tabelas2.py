# Tabelas brasileirão 1971-2002
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
#from recursos import Bases
#bases = Bases()

css_chaves = st.secrets.atalhos.css

def render_html_css(html_path, css_path, height=600, scrolling=True):
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


def mostrar_html(arquivo):
    caminho = st.secrets.atalhos.bd_cb_ff
    with open(caminho + arquivo, "r", encoding="utf-8") as f:
        html = f.read()

    #st.html(html)
    components.html(
        f"<style>{caminho+'definicoes.css'}</style>{html}")


render_html_css(
    html_path = st.secrets.atalhos.bd_cb_ff + "2002CB.html",
    css_path= st.secrets.atalhos.bd_cb_ff + st.secrets.atalhos.css,
    height=700
)
