# Tabelas brasileirão 1971-2002
import streamlit as st
import streamlit.components.v1 as components
#from recursos import Bases
#bases = Bases()

css_chaves = st.secrets.atalhos.css

def mostrar_html(arquivo):
    caminho = st.secrets.atalhos.bd_cb_ff
    with open(caminho + arquivo, "r", encoding="utf-8") as f:
        html = f.read()

    #st.html(html)
    components.html(
        f"<style>{caminho+'definicoes.css'}</style>{html}")

mostrar_html('2002CB.html')

#st.write(st.secrets)