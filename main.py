# Arquivo principal do app
import streamlit as st
import gettext
import os

# Configuração i18n
def setup_translation(lang):
    try:
        localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
        trans = gettext.translation('messages', localedir=localedir, languages=[lang])
        trans.install()
        return trans.gettext
    except FileNotFoundError:
        return gettext.gettext # Fallback para o texto original

# Seletor de Idioma no Sidebar
if 'lang' not in st.session_state:
    st.session_state.lang = 'pt_BR'

selected_lang = st.sidebar.selectbox("Idioma (Language)",
                                     ["Português", "English"], index=0)
st.session_state.lang = selected_lang

# Define a função global _()
_ = setup_translation(st.session_state.lang)

st.set_page_config(page_title = "Repositório Estatístico do Futebol Brasileiro (REFB)",
                   layout='wide', page_icon=  "🇧🇷")
st.header("Repositório Estatístico do Futebol Brasileiro")

# Listagem das páginas do site
estat2_pag = st.Page(
    page = 'paginas/estat2.py',
    title = 'Estat.')

estati_pag = st.Page(
    page = 'paginas/estat_ind.py',
    title = 'Estatísticas individuais')

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
pg = st.navigation({_('Início'):[home_pag],
                    'Campeonato Brasileiro':[tab_pag, ranking_pag],
                    'Times':[jogos_pag, confrontos_pag, estati_pag, estat2_pag],
                    'Para você':[com_pag]
                    })

with st.sidebar:
    #linkedin = "https://raw.githubusercontent.com/doriedson-1/exifa/main/img/linkedin.gif"
    twitter = "https://github.com/doriedson-1/REFB/blob/main/Base_de_dados/Imagens/x.gif?raw=true"

    st.sidebar.caption(
        f"""
        <div style='display: flex; align-items: center;'>
            <a href = 'https://www.x.com/refutbr'><img src='{twitter}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
        </div>
        <br>
        """,
        unsafe_allow_html=True,
)
    st.sidebar.text(_('Versão beta'))

pg.run()
