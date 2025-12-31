# Funções principais
import pandas as pd
import numpy as np

class Bases:
    
    def __init__(self):
        self.base_path = 'Base_de_dados/' 
        self.caminhos = {
            'br': self.base_path + 'Campeonato_brasileiro/',
            'copa': self.base_path + 'Copa_do_Brasil/',
            'mata-mata': self.base_path + 'Mata-mata/'}
    
    def grafia(self, coluna):
        """
        Parameters
        ----------
        coluna : object
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if not isinstance(coluna, object):
            return coluna
        
        # onde é o H
        coluna = coluna.replace("Atlético-PR", "Athletico-PR")
        
        # ' ' FC
        coluna = coluna.replace("Santos", "Santos FC")
        
        # GEC
        coluna = coluna.replace("Goiás", "Goiás EC")
        
        return coluna

    
    def ler(self, arquivo, torneio):
        """
        Parâmetros
        ----------
        arquivo : str
            Nome completo do arquivo que deve ser lido (digite a extensão).
        torneio : str
            Digite 'br' para Camp. Brasileiro, 'copa' para Copa do Brasil e
            'mata-mata' para os confrontos eliminatórios em geral.

        Retorna
        -------
        Pandas.DataFrame
            O dito arquivo.

        """
        
        caminho_base = self.caminhos.get(torneio)
        
        caminho_cheio = caminho_base + arquivo
        
        if arquivo.split('.')[-1] == 'csv':
            try:
                # Tenta ler o arquivo CSV
                df = pd.read_csv(caminho_cheio)
                return df
            
            except FileNotFoundError:
                print("Arquivo não encontrado. Por favor, certifique-se que\
                         o arquivo está na pasta.")
                return pd.DataFrame()
        
        elif arquivo.split('.')[-1] == 'xlsx':
            try:
                # Tenta ler o arquivo excel
                df = pd.read_excel(caminho_cheio)
                return df
                
            except FileNotFoundError:
                print(caminho_cheio)
                print("Arquivo não encontrado. Por favor, certifique-se que \
                         o arquivo está na pasta.")
                return pd.DataFrame()
   
            
    def pontuar(self, arq, gol_m, gol_v):
        """
        Parâmetros
        ----------
        arq : DataFrame (pandas)
            DESCRIPTION.
        gol_m : str
            DESCRIPTION.
        gol_v : str
            DESCRIPTION.

        Retorna
        -------
        O arquivo inicial com adição das colunas de pontos do mandante e do visitante.

        """
        arq['pontos_mandante'] = np.where(
            arq[gol_m] > arq[gol_v],
            3,
            np.where(arq[gol_m] == arq[gol_v], 1, 0))
        arq['pontos_visitante'] = np.where(
            arq[gol_v] > arq[gol_m],
            3,
            np.where(arq[gol_m] == arq[gol_v], 1, 0))
        
        return arq
    
    
    def classifica(self, df, ano = 2020, exportar = False):
        """
        Parameters
        ----------
        df : DataFrame
            Objeto do Pandas.
        ano : int
            Ano do campeonato, o padrão é 2020.
        exportar: Boolean
            'True' caso queira exportar o arquivo final.

        Returns
        -------
        classificacao : DataFrame
        """
        
        # 0. Selecionar o ano e as variáveis necessárias na tabela final
        #df = df[df['ano_campeonato'] == ano]
        df = df[['time_mandante', 'time_visitante', 'gols_mandante',
                'gols_visitante', 'pontos_mandante', 'pontos_visitante']]
        
        
        # 1. Criar DataFrame para os Mandantes
        mandantes = df[['time_mandante', 'gols_mandante',
                        'gols_visitante', 'pontos_mandante']].copy()
        mandantes.columns = ['TIME', 'gols_pro', 'gols_contra', 'pontos']
        
        # 2. Criar DataFrame para os Visitantes
        visitantes = df[['time_visitante', 'gols_visitante',
                         'gols_mandante', 'pontos_visitante']].copy()
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
        if exportar == True:
            classificacao.to_excel(self.caminhos.get('br') + f"TabelaFinal{ano}.xlsx",
                                   sheet_name = str(ano))
        
        return classificacao
        