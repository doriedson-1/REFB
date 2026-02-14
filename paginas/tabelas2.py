# Tabelas brasileirão 1971-2002
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

    # 🔹 Get current theme
    theme = st.get_option("theme.base")  # "light" or "dark"
    print('tema:', theme)

    # 🔹 Inject theme class in body
    html = html.replace("<body>", f'<body class="{theme}">')
    
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

dados = bases.ler('2002fi.csv', 'br')

# Ordena as temporadas
temporadas = sorted(dados['campeonato'].unique(), reverse=True)
    
col_filtro, _ = st.columns([1, 3])
with col_filtro:
    selecao_temp = st.selectbox("Selecione a temporada:", temporadas)
    
    # Filtra o DataFrame
    df_show = dados[dados['campeonato'] == selecao_temp].copy()

st.subheader('Primeira fase')

tab = bases.classifica(df_show, selecao_temp)

# Imagens
tab['codigo_temp'] = tab['TIME'].apply(bases.codigo_clube)
base_url = "https://tmssl.akamaized.net//images/wappen/head/"
tab['ESCUDO'] = tab['codigo_temp'].apply(lambda x: f"{base_url}{x}")

# seleção de colunas
tab = tab.iloc[:, [11,0,1,2,3,4,5,6,7,8,9]]

st.dataframe(tab,
             width='stretch',
             column_config={
                 # Configuração da Imagem
                 "ESCUDO": st.column_config.ImageColumn("", width="small"),
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
             },
             hide_index=True)

# # # # # # 
st.divider()

st.subheader('Fase final')

render_html_css(
    html_path = st.secrets.atalhos.bd_cb_ff + "2002CB.html",
    css_path= st.secrets.atalhos.css,
    height=700)
