# Arquivo principal do app
import streamlit as st

st.set_page_config(page_title = "Repositório Estatístico do Futebol Brasileiro (REFB)",
                   layout='wide', page_icon=  "🇧🇷")
st.header("Repositório Estatístico do Futebol Brasileiro")

# Listagem das páginas do site
tab_pag = st.Page(
    page = 'paginas/tabelas.py',
    title = 'Tabelas finais')

com_pag = st.Page(
    page = 'paginas/comunidade.py',
    title = 'Comunidade')

jogos_pag = st.Page(
    page = 'paginas/duelos.py',
    title = 'Confrontos diretos')

confrontos_pag = st.Page(
    page = 'paginas/confrontos.py',
    title = 'Confrontos eliminatórios')

ranking_pag = st.Page(
    page  = 'paginas/ranking.py',
    title = 'Ranking (pontos corridos)')

home_pag = st.Page(
    page = 'paginas/home.py',
    title = 'Apresentação',
    default = True)


# Barra de navegação
pg = st.navigation({'Início':[home_pag],
                    'Campeonato Brasileiro':[tab_pag, ranking_pag],
                    'Times':[jogos_pag, confrontos_pag],
                    'Para você':[com_pag]
                    })

st.sidebar.text('Versão beta')

pg.run()
