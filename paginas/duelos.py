import streamlit as st
import pandas as pd
import numpy as np
from recursos import Bases

bases = Bases()

def render_confrontos_detalhados(df: pd.DataFrame):
    st.divider()
    st.subheader("⚔️ Confrontos diretos")

    # Listas para os selects
    all_teams = bases.descritivas()
    all_champs = sorted(df['campeonato'].unique())

    # --- INÍCIO DO FORMULÁRIO ---
    with st.form(key="form_analise_duelos"):
        c1, c2, c3 = st.columns([2, 2, 2])

        with c1:
            campeonato = st.selectbox("Campeonato:", ["Todos"] + all_champs)

        with c2:
            # Tenta usar o pré-selecionado se existir
            idx_padrao_a = 0
            
            time_a = st.selectbox("Time:", all_teams, index=idx_padrao_a)

        with c3:
            # Nota: Dentro de um form, não conseguimos excluir o Time A da lista B
            # dinamicamente sem recarregar a página. Usamos a lista completa aqui.
            time_b = st.selectbox("Adversário:", all_teams)

        # O botão que libera o processamento
        submit_button = st.form_submit_button(
            label="Analisar Confrontos", 
            type="primary", 
            #use_container_width=True
            width='stretch'
        )

    # --- LÓGICA PÓS-SUBMISSÃO ---
    if submit_button:
        # 1. Validação simples
        if time_a == time_b:
            st.warning("⚠️ Selecione dois times diferentes para comparar.")
            return

        # 2. Processamento dos Dados
        mask_teams = (
            ((df['time_mandante'] == time_a) & (df['time_visitante'] == time_b)) |
            ((df['time_mandante'] == time_b) & (df['time_visitante'] == time_a))
        )
        
        if campeonato != "Todos":
            mask_final = mask_teams & (df['campeonato'] == campeonato)
        else:
            mask_final = mask_teams

        df_filtered = df[mask_final].copy()

        # 3. Exibição
        if df_filtered.empty:
            st.info(f"Não foram encontrados jogos entre **{time_a}** e **{time_b}** com os filtros atuais.")
        else:
            # Ordenação
            if 'data' in df_filtered.columns:
                df_filtered = df_filtered.sort_values('data', ascending=False)
            
            # Renderiza a tabela
            st.markdown(f"### Histórico: {time_a} x {time_b}")
            _renderizar_tabela_colorida(df_filtered, time_a)
            
            st.write('GolsM = Gols mandante')
            st.write('GolsV = Gols visitante')
            
            # Renderiza estatísticas
            _mostrar_resumo_estatistico(df_filtered, time_a, time_b)


def _renderizar_tabela_colorida(df, time_ref):
    """Função auxiliar para isolar a lógica visual da tabela"""
    
    df = df.copy()
    
    # Converter para Datetime real (para ordenar corretamente e permitir formatação)
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    
    # Converter Gols para Inteiro (remove o .0)
    # O fillna(0) garante que se houver vazio, vira 0 antes de virar int
    if 'gols_mandante' in df.columns:
        df['gols_mandante'] = pd.to_numeric(df['gols_mandante'], errors='coerce').fillna(0).astype(int)
    if 'gols_visitante' in df.columns:
        df['gols_visitante'] = pd.to_numeric(df['gols_visitante'], errors='coerce').fillna(0).astype(int)
    
    def style_row(row):
        gols_a = row['gols_mandante'] if row['time_mandante'] == time_ref else row['gols_visitante']
        gols_b = row['gols_visitante'] if row['time_mandante'] == time_ref else row['gols_mandante']
        
        if gols_a > gols_b:
            return ['background-color: #d4edda; color: #155724'] * len(row)
        elif gols_a < gols_b:
            return ['background-color: #f8d7da; color: #721c24'] * len(row)
        else:
            return ['background-color: #fff3cd; color: #856404'] * len(row)

    cols_display = ['data', 'campeonato', 'time_mandante', 'gols_mandante',
                    'gols_visitante', 'time_visitante']
    cols_final = [c for c in cols_display if c in df.columns]
    
    st.dataframe(
        df[cols_final].style.apply(style_row, axis=1),
        #use_container_width=True,
        width = 'stretch',
        hide_index=True,
        column_config={
            "data": st.column_config.DateColumn(
                "Data",             # Título que aparece na tela
                #format="DD/MM/YYYY" # Formato brasileiro
            ),
            "campeonato": st.column_config.TextColumn("Campeonato"),
            "time_mandante": st.column_config.TextColumn("Mandante"),
            "time_visitante": st.column_config.TextColumn("Visitante"),
            "gols_mandante": st.column_config.NumberColumn(
                "GolsM", 
                format="%d"         # %d força mostrar como inteiro sem vírgula
            ),
            "gols_visitante": st.column_config.NumberColumn(
                "GolsV", 
                format="%d"
            )
        }
    )


def _mostrar_resumo_estatistico(df: pd.DataFrame, time_a: str, time_b: str):
    """
    Calcula e exibe as estatísticas agregadas.
    Função auxiliar privada para manter o código limpo.
    """
    # Vetorização para cálculo rápido
    # Condições onde A é mandante
    is_a_home = df['time_mandante'] == time_a
    
    # Gols marcados por A e B
    gols_a = np.where(is_a_home, df['gols_mandante'], df['gols_visitante'])
    gols_b = np.where(is_a_home, df['gols_visitante'], df['gols_mandante'])

    total_jogos = len(df)
    vitorias = np.sum(gols_a > gols_b)
    derrotas = np.sum(gols_a < gols_b)
    empates  = np.sum(gols_a == gols_b)
    
    st.markdown("---")
    st.subheader("📊 Resumo")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Jogos", total_jogos)
    with col2:
        st.metric(f"Vitórias {time_a}", int(vitorias),
                  delta=f"{(vitorias/total_jogos)*100:.1f}%" if total_jogos else None)
    with col3:
        st.metric("Empates", int(empates))
    with col4:
        st.metric(f"Vitórias {time_b}", int(derrotas), delta_color="inverse")


df = bases.ler('pontos_corridos.xlsx', 'br')
df['campeonato'] = 'Brasileiro'

# Correções ortográficas
df['time_mandante']= bases.grafia(df['time_mandante'])
df['time_visitante'] = bases.grafia(df['time_visitante'])

st.write('No momento só há duelos do campeonato brasileiro (desde 2003)!')

render_confrontos_detalhados(df)
