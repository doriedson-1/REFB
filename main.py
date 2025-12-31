# Arquivo principal do app
from config import *
import streamlit as st

st.set_page_config(page_title = "R.E.F.B", layout='wide', page_icon=  "🇧🇷")
st.header("Repositório Estatístico do Futebol Brasileiro")

# Listagem das páginas do site
confrontos_pag = st.Page(
    page = 'paginas/confrontos.py',
    title = 'Confrontos eliminatórios')

home_pag = st.Page(
    page = 'paginas/home.py',
    title = 'Apresentação',
    default = True)


# Barra de navegação
pg = st.navigation([home_pag, confrontos_pag])

st.sidebar.text('Versão beta')

pg.run()

