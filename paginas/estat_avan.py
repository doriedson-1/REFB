# Estatísticas avançadas de jogadores
import pandas as pd
import numpy as np
import streamlit as st
from recursos import Bases
from mplsoccer import Pitch, VerticalPitch

bases = Bases()

@st.cache_data
def ler_parquet(arquivo):
    return pd.read_parquet(arquivo)

def show_rankings(df):
    st.markdown("### 📊 Rankings de Jogadores")

    # ----------------------------
    # FILTROS
    # ----------------------------
    teams = sorted(df['teamName'].dropna().unique())
    team_filter = st.selectbox("Selecione o time (ou Todos):", ["Todos"] + teams)

    min_games = st.number_input("Número mínimo de jogos:", min_value=1, value=1)

    mode = st.radio("Modo de visualização:", ["Total", "Por jogo"])

    # ----------------------------
    # CÁLCULO DE MÉTRICAS
    # ----------------------------
    # contar jogos distintos por jogador
    games_played = df.groupby("playerName")["matchId"].nunique().reset_index()
    games_played.columns = ["playerName", "Jogos"]

    # agregar métricas
    agg_funcs = {
        # Passes
        "passAccurate": "sum",
        "passInaccurate": "sum",
        "box_entry": "sum",
        "progressive_action": "sum",
        "last_third_entry": "sum",

        # Ataque
        "isGoal": "sum",
        "assist": "sum",
        "passKey": "sum",
        "passCornerAccurate": "sum",
        "passCornerInaccurate": "sum",
        "shotsTotal": "sum",
        "shotOnTarget": "sum",
        "shotOffTarget": "sum",
        "shotOnPost": "sum",
        "dribbleWon": "sum",
        "dribbleLost": "sum",

        # Defesa
        "tackleWon": "sum",
        "tackleLost": "sum",
        "ballRecovery": "sum",
        "clearanceTotal": "sum",
        "interceptionAll": "sum",
        "foulCommitted": "sum",
    }

    stats = df.groupby(["playerName", "teamName"]).agg(agg_funcs).reset_index()
    stats = stats.merge(games_played, on="playerName", how="left")

    # calcular derivados
    stats["Passes Totais"] = stats["passAccurate"] + stats["passInaccurate"]
    stats["Passes Certos"] = stats["passAccurate"]
    stats["Passes Errados"] = stats["passInaccurate"]
    stats["Aproveitamento nos Passes"] = (stats["passAccurate"] / stats["Passes Totais"] * 100).round(1)

    stats["Passes para a Área"] = stats["box_entry"]
    stats["Passes Progressivos"] = stats["progressive_action"]
    stats["Passes para o Terço Final"] = stats["last_third_entry"]

    stats["Gols"] = stats["isGoal"]
    stats["Assistências"] = stats["assist"]
    stats["Chances Criadas"] = stats["passKey"]

    stats["Escanteios Certos"] = stats["passCornerAccurate"]
    stats["Escanteios Errados"] = stats["passCornerInaccurate"]
    stats["Acerto nos Escanteios"] = (stats["passCornerAccurate"] / (stats["passCornerAccurate"] + stats["passCornerInaccurate"]) * 100).round(1)

    stats["Finalizações"] = stats["shotsTotal"]
    stats["Finalizações no Alvo"] = stats["shotOnTarget"]
    stats["Finalizações pra Fora"] = stats["shotOffTarget"]
    stats["Finalizações na Trave"] = stats["shotOnPost"]
    stats["Taxa de Conversão"] = (stats["isGoal"] / stats["shotsTotal"] * 100).round(1)
    stats["Aproveitamento nas Finalizações"] = (stats["shotOnTarget"] / stats["shotsTotal"] * 100).round(1)

    stats["Dribles Totais"] = stats["dribbleWon"] + stats["dribbleLost"]
    stats["Dribles Corretos"] = stats["dribbleWon"]
    stats["Dribles Errados"] = stats["dribbleLost"]
    stats["Aproveitamento nos Dribles"] = (stats["dribbleWon"] / stats["Dribles Totais"] * 100).round(1)

    stats["Desarmes"] = stats["tackleWon"] + stats["tackleLost"]
    stats["Bolas Recuperadas"] = stats["ballRecovery"]
    stats["Rebatidas"] = stats["clearanceTotal"]
    stats["Interceptações"] = stats["interceptionAll"]
    stats["Faltas"] = stats["foulCommitted"]

    # ----------------------------
    # AJUSTE TOTAL vs POR JOGO
    # ----------------------------
    if mode == "Por jogo":
        for col in [
            "Passes Totais", "Passes Certos", "Passes Errados", "Passes para a Área",
            "Passes Progressivos", "Passes para o Terço Final",
            "Gols", "Assistências", "Chances Criadas",
            "Escanteios Certos", "Escanteios Errados",
            "Finalizações", "Finalizações no Alvo", "Finalizações pra Fora", "Finalizações na Trave",
            "Dribles Totais", "Dribles Corretos", "Dribles Errados",
            "Desarmes", "Bolas Recuperadas", "Rebatidas", "Interceptações", "Faltas"
        ]:
            stats[col] = (stats[col] / stats["Jogos"]).round(2)

    # ----------------------------
    # FILTROS FINAIS
    # ----------------------------
    if team_filter != "Todos":
        stats = stats[stats["teamName"] == team_filter]

    stats = stats[stats["Jogos"] >= min_games]

    # ----------------------------
    # TABELAS
    # ----------------------------
    st.subheader("🎯 Passes")
    st.dataframe(stats[["playerName", "teamName", "Jogos", "Passes Totais",
                        "Passes Certos", "Passes Errados", "Aproveitamento nos Passes",
                        "Passes para a Área", "Passes Progressivos",
                        "Passes para o Terço Final"]],
                column_config={
                    "playerName": st.column_config.TextColumn("Jogador", width="medium"),
                    "teamName": st.column_config.TextColumn("Time", width="medium")
                    })

    st.subheader("⚡ Ataque")
    st.dataframe(stats[["playerName", "teamName", "Jogos",
                        "Gols", "Assistências", "Chances Criadas",
                        "Escanteios Certos", "Escanteios Errados", "Acerto nos Escanteios",
                        "Finalizações", "Finalizações no Alvo", "Finalizações pra Fora",
                        "Finalizações na Trave", "Taxa de Conversão",
                        "Aproveitamento nas Finalizações", "Dribles Totais",
                        "Dribles Corretos", "Dribles Errados",
                        "Aproveitamento nos Dribles"]],
                column_config={
                    "playerName": st.column_config.TextColumn("Jogador", width="medium"),
                    "teamName": st.column_config.TextColumn("Time", width="medium")
                    })

    st.subheader("🛡️ Defesa")
    st.dataframe(stats[["playerName", "teamName", "Jogos", "Desarmes",
                        "Bolas Recuperadas", "Rebatidas", "Interceptações",
                        "Faltas"]],
                column_config={
                    "playerName": st.column_config.TextColumn("Jogador", width="medium"),
                    "teamName": st.column_config.TextColumn("Time", width="medium")
                    })


caminho = bases.caminhos['br']
df = ler_parquet(caminho + 'BRA25.parquet')

#st.dataframe(df.head(200), width='stretch')
#a=len(df); st.write(a)

df['teamName'] = df['teamId'].map(
    lambda team_id: bases.codigo_clube(team_id, local='parquet'))

df['away'] = bases.grafia(df['away'])
df['home'] = bases.grafia(df['home'])

#todos_times = sorted(df['TIME'].dropna().unique())

show_rankings(df)

#nomes = bases.grafia(nomes)

st.write('Em atualização...')
