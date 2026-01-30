# Página inicial
import streamlit as st

st.markdown('### Bem vindos(as)!')

st.text('No REFB você encontra visualizações do futebol brasileiro de maneira intuitiva.')

<details>

<summary>Tips for collapsed sections</summary>

### You can add a header

You can add text within a collapsed section.

You can add an image or a code block, too.

```ruby
   puts "Hello World"
```

</details>

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
