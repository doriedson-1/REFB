import pandas as pd
import streamlit as st
from recursos import Bases

# Instância
bases = Bases()

def render_confrontos_detalhados(df: pd.DataFrame):
    st.divider()
    st.subheader("⚔️ Análise de Confrontos Diretos")

    # --- 1. Inicialização do Estado para o RESULTADO ---
    # Aqui guardamos o DataFrame JÁ filtrado. Se a página recarregar, o dado está salvo.
    if "df_confronto_resultado" not in st.session_state:
        st.session_state["df_confronto_resultado"] = None
    if "meta_dados_confronto" not in st.session_state:
        st.session_state["meta_dados_confronto"] = {}

    # Prepara listas
    all_teams = sorted(pd.concat([df['time_mandante'], df['time_visitante']]).unique())
    all_champs = sorted(df['campeonato'].unique())

    # --- 2. Formulário (Garante que a página não recarrega enquanto escolhe) ---
    with st.form(key="form_analise_duelos"):
        c1, c2, c3 = st.columns([2, 2, 2])
        
        with c1:
            camp_input = st.selectbox("Campeonato:", ["Todos"] + all_champs)
        with c2:
            time_a_input = st.selectbox("Time A (Referência):", all_teams)
        with c3:
            time_b_input = st.selectbox("Time B (Oponente):", all_teams)

        submit = st.form_submit_button("Analisar Confrontos", type="primary", use_container_width=True)

    # --- 3. Lógica de Processamento (Só roda no clique) ---
    if submit:
        if time_a_input == time_b_input:
            st.warning("⚠️ Selecione dois times diferentes.")
        else:
            # Filtra os dados
            mask = (
                ((df['time_mandante'] == time_a_input) & (df['time_visitante'] == time_b_input)) |
                ((df['time_mandante'] == time_b_input) & (df['time_visitante'] == time_a_input))
            )
            
            if camp_input != "Todos":
                mask = mask & (df['campeonato'] == camp_input)

            df_res = df[mask].copy()
            
            # Ordena
            if 'data' in df_res.columns:
                df_res = df_res.sort_values('data', ascending=False)
            
            # --- TRUQUE DE VISUALIZAÇÃO (Sem Pandas Styler) ---
            # Criamos colunas amigáveis para exibição direta
            if not df_res.empty:
                # Determina o resultado visualmente com texto/emojis
                def get_resultado(row):
                    gols_a = row['gols_mandante'] if row['time_mandante'] == time_a_input else row['gols_visitante']
                    gols_b = row['gols_visitante'] if row['time_mandante'] == time_a_input else row['gols_mandante']
                    
                    if gols_a > gols_b: return "✅ Vitória"
                    elif gols_a < gols_b: return "❌ Derrota"
                    return "➖ Empate"

                df_res['Resultado'] = df_res.apply(get_resultado, axis=1)
                
                # Formatamos o placar "3 x 1" para ficar bonito
                df_res['Placar'] = df_res.apply(lambda x: f"{int(x['gols_mandante'])} x {int(x['gols_visitante'])}", axis=1)

            # Salva no estado
            st.session_state["df_confronto_resultado"] = df_res
            st.session_state["meta_dados_confronto"] = {"time_a": time_a_input, "time_b": time_b_input}

    # --- 4. Exibição (Lê do Estado) ---
    df_show = st.session_state["df_confronto_resultado"]
    meta = st.session_state["meta_dados_confronto"]

    if df_show is not None:
        if df_show.empty:
            st.info("Nenhum jogo encontrado com estes filtros.")
        else:
            t_a = meta.get("time_a")
            t_b = meta.get("time_b")
            
            st.markdown(f"### Resultados: {t_a} x {t_b}")
            
            # Seleciona colunas limpas para mostrar (sem a complexidade do styler)
            cols_to_show = ['data', 'campeonato', 'time_mandante', 'Placar', 'time_visitante', 'Resultado']
            
            # Filtra colunas que realmente existem
            cols_final = [c for c in cols_to_show if c in df_show.columns]

            st.dataframe(
                df_show[cols_final],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Resultado": st.column_config.TextColumn(
                        "Status",
                        help="Resultado para o Time A",
                        width="small"
                    ),
                    "Placar": st.column_config.TextColumn(
                        "Placar",
                        width="small"
                    )
                }
            )
            
            # Estatísticas (Opcional)
            _mostrar_estatisticas_simples(df_show, t_a)


def _mostrar_estatisticas_simples(df, time_a):
    """Cálculo simples baseado na coluna Resultado que criamos"""
    if 'Resultado' not in df.columns: return

    vit = len(df[df['Resultado'] == "✅ Vitória"])
    der = len(df[df['Resultado'] == "❌ Derrota"])
    emp = len(df[df['Resultado'] == "➖ Empate"])
    total = len(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jogos", total)
    col2.metric("Vitórias", vit, delta="Venceu" if vit > der else None)
    col3.metric("Empates", emp)
    col4.metric("Derrotas", der, delta_color="inverse")


# --- EXECUÇÃO ---
# Carregamento e Tratamento Inicial
df = bases.ler('pontos_corridos.xlsx', 'br')
df['campeonato'] = 'Brasileiro'

# Padronização de nomes de coluna (Minúsculo e sem espaços)
df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]

if 'time_mandante' in df.columns:
    df['time_mandante'] = bases.grafia(df['time_mandante'])
if 'time_visitante' in df.columns:
    df['time_visitante'] = bases.grafia(df['time_visitante'])

render_confrontos_detalhados(df)