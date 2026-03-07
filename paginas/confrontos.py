import pandas as pd
import streamlit as st
from recursos import Bases

# Instância
bases = Bases()

# Carregar os dados
df = bases.ler('confrontos.csv', 'mata-mata')

if not df.empty:
    # Matriz Quadrada
    todos_times = sorted(list(set(df['Vencedor']).union(set(df['Perdedor']))))

    # Cria a tabela cruzada
    matrix = pd.crosstab(df['Vencedor'], df['Perdedor'])

    # Reindexa para garantir que todos os times apareçam nas linhas e colunas (matriz quadrada)
    matrix = matrix.reindex(index=todos_times, columns=todos_times, fill_value=0)

    # 3. Dicionário de Cores dos Times (Personalizado)
    # Cores aproximadas para garantir leitura com texto branco
    team_colors = {
        'Palmeiras': "#006437CC",    # Verde Escuro
        'Corinthians': '#111111CC',  # Preto
        'São Paulo': '#FE0000CC',    # Vermelho
        'Santos': '#000000CC',       # Preto
        'Flamengo': '#C3281ECC',     # Vermelho Rubro-Negro
        'Vasco': '#333333CC',        # Cinza Chumbo/Preto
        'Fluminense': '#9F022FCC',   # Grená
        'Botafogo': '#222222CC',     # Preto
        'Grêmio': '#0D80BFCC',       # Azul Grêmio
        'Internacional': '#E20E0ECC',# Vermelho Inter
        'Cruzeiro': '#0055A4CC',     # Azul Cruzeiro
        'Atlético': '#000000CC',     # Preto
    }

NEUTRAL_COLOR = "#AAAAAA"

st.subheader('Confrontos')

st.markdown('Histórico de enfrentamento do G12 do futebol brasileiro em decisões por\
         competições oficiais. Estão inclusas partidas dos seguintes torneios:\
         Campeonato Brasileiro, Copa do Brasil, Copa dos Campeões, Supercopa do Brasil,\
         Copa Libertadores da América, Supercopa da Libertadores, Copa Mercosul,\
         Copa Sulamericana, Copa Conmebol, Copa Ouro, Copa Master da Supercopa, \
         Copa Master da Conmebol, Torneio Rio-São Paulo, Torneio Sul-Minas\
         (incluindo a Copa Sul-Minas-Rio) e torneios oficiais da FIFA, :red[exceto]\
         os mata-matas válidos pelos estaduais')

if not df.empty:
    # Lista de times única e ordenada
    todos_times = sorted(list(set(df['Vencedor']).union(set(df['Perdedor']))))

    # Preparar Matriz de Placar
    raw_counts = pd.crosstab(df['Vencedor'], df['Perdedor'])
    raw_counts = raw_counts.reindex(index=todos_times, columns=todos_times, fill_value=0)

    display_df = pd.DataFrame(index=todos_times, columns=todos_times)
    style_df = pd.DataFrame(index=todos_times, columns=todos_times)

    for time_A in todos_times:
        for time_B in todos_times:
            if time_A == time_B:
                display_df.at[time_A, time_B] = "—"
                style_df.at[time_A, time_B] = "background-color: #F5F5F5; color: #F5F5F5"
            else:
                wins_A = raw_counts.at[time_A, time_B]
                wins_B = raw_counts.at[time_B, time_A]
                display_df.at[time_A, time_B] = f"{wins_A} x {wins_B}"

                if wins_A > wins_B:
                    cor = team_colors.get(time_A, '#555555')
                    style_df.at[time_A, time_B] = f"background-color: {cor}; color: white; font-weight: bold"
                elif wins_B > wins_A:
                    cor = team_colors.get(time_B, '#555555')
                    style_df.at[time_A, time_B] = f"background-color: {cor}; color: white; font-weight: bold"
                else:
                    if wins_A == 0 and wins_B == 0:
                         style_df.at[time_A, time_B] = "color: #DDDDDD" # Quase invisível
                    else:
                         style_df.at[time_A, time_B] = f"background-color: {NEUTRAL_COLOR}; color: white; font-weight: bold"

    # Exibir Matriz com Seleção
    
    st.markdown("💡 Selecione um time na linha para carregar os detalhes abaixo.")
    
    # Cálculo dinâmico da altura: (num_linhas + cabeçalho) * pixels_por_linha
    height_dynamic = (len(todos_times) + 1) * 35 + 3

    # Exibe a tabela permitindo selecionar a linha
    event = st.dataframe(
        display_df.style.apply(lambda x: style_df, axis=None),
        height=height_dynamic, # Altura ajustada
        width = 'stretch',
        on_select="rerun",     # Recarrega a página ao clicar
        selection_mode="single-row" 
    )

    # Área de Detalhes
    st.divider()
    st.subheader("🔎 Detalhes")

    col1, col2 = st.columns(2)

    # Lógica de Seleção Automática baseada no clique
    time_selecionado_tabela = None
    if len(event.selection['rows']) > 0:
        idx_row = event.selection['rows'][0]
        time_selecionado_tabela = display_df.index[idx_row]

    with col1:
        # Se clicou na tabela, o valor padrão muda para o time clicado
        index_padrao = 0
        if time_selecionado_tabela and time_selecionado_tabela in todos_times:
            index_padrao = todos_times.index(time_selecionado_tabela)
            
        time_a = st.selectbox("Time A:", todos_times, index=index_padrao)

    with col2:
        # O segundo selectbox exclui o time A para não comparar com ele mesmo
        oponentes = [t for t in todos_times if t != time_a]
        time_b = st.selectbox("Time B:", oponentes)

    # Filtrar os jogos
    if time_a and time_b:
        mask = ((df['Vencedor'] == time_a) & (df['Perdedor'] == time_b)) | \
               ((df['Vencedor'] == time_b) & (df['Perdedor'] == time_a))
        
        jogos = df[mask].sort_values('Ano', ascending=False) # Mais recentes primeiro

        if jogos.empty:
            st.info(f"Não há registros de confrontos eliminatórios/finais entre **{time_a}** e **{time_b}** neste arquivo.")
        else:
            # Placar Geral
            vitorias_a = len(jogos[jogos['Vencedor'] == time_a])
            vitorias_b = len(jogos[jogos['Vencedor'] == time_b])
            
            st.markdown(f"### Placar Geral: {time_a} <span style='color:{team_colors.get(time_a, 'black')}'>{vitorias_a}</span> x <span style='color:{team_colors.get(time_b, 'black')}'>{vitorias_b}</span> {time_b}", unsafe_allow_html=True)
            
            # Formatação visual da tabela de detalhes
            def highlight_winner(row):
                # Pinta a linha de verde leve se o Time A ganhou, vermelho leve se perdeu
                if row['Vencedor'] == time_a:
                    return ['background-color: #d4edda; color: #155724'] * len(row)
                else:
                    return ['background-color: #f8d7da; color: #721c24'] * len(row)

            st.dataframe(
                jogos[['Ano', 'Campeonato', 'Fase', 'Vencedor']].style.apply(highlight_winner, axis=1),
                #use_container_width=True,
                width = 'stretch',
                hide_index=True
            )