# Página inicial
import streamlit as st

st.markdown('### Bem vindos(as)!')

st.text('No REFB você encontra visualizações do futebol brasileiro de maneira intuitiva.')

st.markdown('#### Links')

with st.expander('Campeonato brasileiro'):
    st.markdown('- [Tabelas finais dos pontos corridos](https://refutbr.streamlit.app/tabelas)')
    st.markdown('- [Tabela acumulada pontos corridos](https://refutbr.streamlit.app/ranking)')
    st.markdown('- Era do mata-mata (1971-2002) [Em breve]')

with st.expander('Histórico de confrontos'):
    st.markdown('- [Time contra time (considera apenas os confrontos da base de dados)](https://refutbr.streamlit.app/duelos)')
    st.markdown('- [Confrontos eliminatórios do G12](https://refutbr.streamlit.app/confrontos)')

#st.markdown('Contribua no [github](https://github.com/doriedson-1/REFB)!')

st.divider()
st.subheader('Fontes')

st.markdown('[Base dos dados](https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23?table=18835b0d-233e-4857-b454-1fa34a81b4fa)')
st.markdown('[Campeões do futebol](https://www.campeoesdofutebol.com.br/brasileiro_ranking_pontos_corridos.html)')
st.markdown('[CBF](https://cbf.com.br/futebol-brasileiro)')
st.markdown('[Futdados](https://futdados.com/)')
st.markdown('[Sinopse do futebol](https://sinopsedofutebol.blogspot.com/2011/01/mata-matas-decisoes-e-confrontos.html)')

st.divider()
st.subheader('Referências')
st.markdown('[RSSSF Brasil](https://rsssfbrasil.com/)') # o maior de todos

st.divider()
st.write('Outras informações')
st.markdown('[Licença](https://opensource.org/license/mit)')
