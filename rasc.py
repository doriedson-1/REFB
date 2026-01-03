import pandas as pd
from recursos import Bases


bases = Bases()

def addc(ano):
     nome = f"Base_de_dados/Campeonato_brasileiro/TabelaFinal{ano}.xlsx"
     df = pd.read_excel(nome)
     df['CAMPEONATO'] = ano
     
     df.to_excel(nome, index = False)
     print(df)


def concatenar(inicio, fim):
    excel_names = [f"Base_de_dados/Campeonato_brasileiro/TabelaFinal{ano}.xlsx" for ano in range(inicio,fim+1)]
    
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
    
    
# =============================================================================
# arquivo = 'C:/REFB/Brasileirao2004.csv'
# arq = pd.read_csv(arquivo)
# arq['time_mandante'] = bases.grafia(arq['time_mandante'])
# arq['time_visitante'] = bases.grafia(arq['time_visitante'])
# arq = bases.classifica(arq)
# 
# =============================================================================

concatenar(2003, 2004)
