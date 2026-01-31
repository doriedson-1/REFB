# Página inicial
import streamlit as st
from main import setup_translation

_ = setup_translation(st.session_state.lang)

st.markdown(_('### Bem vindos(as)!'))

st.markdown(_('No REFB, é possível explorar informações de vários campeonatos, facilitando \
        análises históricas, comparações entre temporadas e acompanhamento do \
        desempenho de clubes ao longo dos anos. A plataforma está em constante \
        evolução e será gradualmente ampliada, incorporando novos dados, \
        funcionalidades e competições, com o objetivo de se tornar uma referência \
        para torcedores, analistas e entusiastas do futebol nacional.'))

st.markdown('##### Links')

with st.expander('Campeonato brasileiro'):
    st.page_link('paginas/tabelas.py', label = '\- Tabelas (2003-2025)')
    st.page_link('paginas/ranking.py', label = '\- Tabela acumulada pontos corridos')
    st.markdown('Era do mata-mata (1971-2002) [Em breve]')

with st.expander('Histórico de confrontos'):
    st.page_link('paginas/duelos.py', label = 'Time contra time')
    st.page_link('paginas/confrontos.py', label = 'Confrontos eliminatórios do G12')

#st.markdown('Contribua no [github](https://github.com/doriedson-1/REFB)!')

st.divider()
st.subheader(_('Fontes'))

st.markdown('[Base dos dados](https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23?table=18835b0d-233e-4857-b454-1fa34a81b4fa)')
st.markdown('[Campeões do futebol](https://www.campeoesdofutebol.com.br/brasileiro_ranking_pontos_corridos.html)')
st.markdown('[CBF](https://cbf.com.br/futebol-brasileiro)')
st.markdown('[Futdados](https://futdados.com/)')
st.markdown('[Sinopse do futebol](https://sinopsedofutebol.blogspot.com/2011/01/mata-matas-decisoes-e-confrontos.html)')

st.divider()
st.subheader(_('Referências'))
st.markdown('[RSSSF Brasil](https://rsssfbrasil.com/)') # o maior de todos

st.divider()
st.write(_('Outras informações'))
st.markdown(_('[Licença](https://opensource.org/license/mit)'))
