import numpy as np
import pandas as pd
from config import *

#arq = pd.read_excel(BASE_PATH + BRASILEIRAO, sheet_name='2025')

#bd = pd.read_excel(BASE_PATH + CB + 'basedosdados_campeonatos.xlsx')


def pontuar(arquivo, nome_coluna="Placar"):
    '''
    Recebe um data frame (pandas) e separa a coluna de placar, além de fazer a
    atribuição de pontos.'''
    
    # Separação do placar
    _placar = arquivo[nome_coluna].str.split("x", expand = True).astype(int)
    
    arquivo["Gols (Casa)"] = _placar[0]
    arquivo["Gols (Visitante)"] = _placar[1]

    # Contagem de pontos
    arquivo["Pontos (Casa)"] = np.where(
        _placar[0] > _placar[1],
        3,
        np.where(_placar[0] == _placar[1], 1, 0))
    
    arquivo["Pontos (Visitante)"] = np.where(
        _placar[1] > _placar[0],
        3,
        np.where(_placar[0] == _placar[1], 1, 0))
    
    return arquivo


def classific(df, campeonato, ano):
    '''Recebe a tabela de jogos completa (def pontuar) e cria a tabela
    de classificação.
    '''
    
    # 1. Criar DataFrame para os Mandantes
    mandantes = df[['Time 1 (Casa)', 'Gols (Casa)',
                    'Gols (Visitante)', 'Pontos (Casa)']].copy()
    mandantes.columns = ['TIME', 'gols_pro', 'gols_contra', 'pontos']
    
    # 2. Criar DataFrame para os Visitantes
    visitantes = df[['Time 2 (Visitante)', 'Gols (Visitante)',
                     'Gols (Casa)', 'Pontos (Visitante)']].copy()
    visitantes.columns = ['TIME', 'gols_pro', 'gols_contra', 'pontos']
    
    # 3. Concatenar (empilhar) os dois
    tabela = pd.concat([mandantes, visitantes], ignore_index=True)
    
    # 3.1 Contagem de resultados
    tabela['vitorias'] = (tabela['pontos'] == 3).astype(int)
    tabela['empates'] = (tabela['pontos'] == 1).astype(int)
    tabela['derrotas'] = (tabela['pontos'] == 0).astype(int)
  
    # 4. Agrupar por TIME e somar as estatísticas
    classificacao = tabela.groupby('TIME').agg({
        'pontos': 'sum',
        'vitorias': 'sum',
        'empates': 'sum',
        'derrotas': 'sum',
        'gols_pro': 'sum',
        'gols_contra': 'sum'
    })
    
    # 5. Criar colunas extras (Saldo de Gols e Jogos)
    classificacao['saldo_gols'] = classificacao['gols_pro'] - classificacao['gols_contra']
    classificacao['jogos'] = tabela.groupby('TIME').size()
    classificacao['aproveitamento'] = (
        (classificacao['pontos']/(classificacao['jogos'] * 3)) * 100).round(1)
    
    # 6. Ordenar pelos critérios oficiais (Pontos, depois Saldo, depois Gols Pro)
    classificacao = classificacao.sort_values(
        by=['pontos', 'saldo_gols', 'gols_pro'], 
        ascending=False
    )
    
    # 7. Formatação
    classificacao.rename(columns = {'pontos':'PONTOS', 'vitorias':'VITORIAS',
                                    'empates':'EMPATES', 'derrotas':'DERROTAS',
                                    'gols_pro':'GOLS_PRO',
                                    'gols_contra':'GOLS_CONTRA',
                                    'saldo_gols':'SALDO_GOLS', 'jogos':'JOGOS',
                                    'aproveitamento':'APROVEITAMENTO'},
                         inplace = True)
    
    # 8. Exportação
    classificacao.to_excel(BASE_PATH + CB + campeonato + ".xlsx",
                           sheet_name = str(ano))
    
    return classificacao

def padronizar_n(coluna):
    '''Recebe uma coluna de data frame (pandas) e retorna a mesma coluna com os
    tratamentos aplicados.
    '''
    if not isinstance(coluna, object):
        return coluna
    
    # onde é o H
    coluna = coluna.replace("Atlético-PR", "Athletico-PR")
    
    # ' ' FC
    coluna = coluna.replace("Santos", "Santos FC")
    
    # GEC
    coluna = coluna.replace("Goiás", "Goiás EC")
    
    return coluna
    


# =============================================================================
# def addc(ano):
#     nome = f"Base_de_dados/Campeonato_brasileiro/TabelaFinal{ano}.xlsx"
#     df = pd.read_excel(nome)
#     df['CAMPEONATO'] = ano
#     
#     df.to_excel(nome, index = False)
#     print(df)
#     
#     
# =============================================================================


    
excel_names = [f"Base_de_dados/Campeonato_brasileiro/TabelaFinal{ano}.xlsx" for ano in range(2005, 2024)]

# read them in
excels = [pd.ExcelFile(name) for name in excel_names]

# turn them into dataframes
frames = [x.parse(x.sheet_names[0], header=None, index_col=None) for x in excels]

# delete the first row for all frames except the first
# i.e. remove the header row -- assumes it's the first
frames[1:] = [df[1:] for df in frames[1:]]

# concatenate them..
combined = pd.concat(frames)

# write it out
combined.to_excel("TabelaFinal.xlsx", header=False, index=False)
