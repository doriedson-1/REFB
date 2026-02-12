# Funções principais
import pandas as pd
import numpy as np
import streamlit as st

class Bases:
    
    def __init__(self):
        self.base_path = 'Base_de_dados/' 
        self.caminhos = {
            'br': self.base_path + 'Campeonato_brasileiro/',
            'copa': self.base_path + 'Copa_do_Brasil/',
            'mata-mata': self.base_path + 'Mata-mata/',
            'lib': self.base_path + 'Libertadores/'}
    
    
    def classifica(self, df, ano = 2020, exportar = False):
        """
        Retorna a classificação final a partir da tabela de jogos.
        ----------
        df : DataFrame
            Objeto do Pandas.
        ano : int
            Ano do campeonato, o padrão é 2020.
        exportar: Boolean
            'True' caso queira exportar o arquivo final.

        Returns
        -------
        classificacao (TabelaFinal) : DataFrame
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
    
    
    def codigo_clube(self, nome_clube):
        """
        """
        # Dicionário de exemplo (substitua pelos seus códigos reais)
        codigos = {
            'América-MG':'2863.png?lm=1646322335',
            'América-RN':'1751.png?lm=1450820578',
            'Athletico-PR':'679.png?lm=1548711363',
            'Atlético-GO':'15172.png?lm=1598605472',
            'Atlético-MG':'330.png?lm=1411033853',
            'Avaí FC':'2035.png?lm=1419949249',
            'Barueri':'8698.png?lm=1455960413',
            'Botafogo':'537.png?lm=1651494898',
            'Brasiliense':'3973.png?lm=1455824776',
            'CSA':'18545.png?lm=1445634683',
            'Ceará SC':'2029.png?lm=1437429449',
            'Chapecoense':'17776.png?lm=1677130387',
            'Corinthians':'199.png?lm=1649430398',
            'Coritiba FC':'776.png?lm=1412879464',
            'Criciúma EC':'7178.png?lm=1412878993',
            'Cruzeiro':'609.png?lm=1757639240',
            'Cuiabá':'28022.png?lm=1451243370',
            'EC Bahia':'10010.png?lm=1412879423',
            'EC Vitória':'2125.png?lm=1412879373',
            'Figueirense FC':'4064.png?lm=1412879618',
            'Flamengo':'614.png?lm=1551023331',
            'Fluminense':'2462.png?lm=1648225934',
            'Fortaleza EC':'10870.png?lm=1631541450',
            'Goiás EC':'3197.png?lm=1668099048',
            'Grêmio':'210.png?lm=1412879265',
            'Guarani':'1755.png?lm=1450819625',
            'Internacional':'6600.png?lm=1644878605',
            'Ipatinga FC':'3270.png?lm=1463474815',
            'Joinville-SC':'3330.png?lm=1419949314',
            'Juventude':'10492.png?lm=1416046262',
            'Mirassol':'3876.png?lm=1585083395',
            'Náutico':'2646.png?lm=1429043382',
            'Palmeiras':'1023.png?lm=1411204983',
            'Paraná':'309.png?lm=1435963615',
            'Paysandu SC':'6347.png?lm=1769784741',
            'Ponte Preta':'1134.png?lm=1419949200',
            'Portuguesa':'10247.png?lm=1673282057',
            'RB Bragantino':'8793.png?lm=1577915313',
            'Santa Cruz':'1785.png?lm=1769785782',
            'Santo André':'7478.png?lm=1450820536',
            'Santos FC':'221.png?lm=1412879099',
            'Sport Recife':'8718.png?lm=1708623979',
            'São Caetano':'291.png?lm=1455314787',
            'São Paulo':'585.png?lm=1409133922',
            'Vasco da Gama':'978.png?lm=1651168164'
        }
        
        # Retorna o código se existir, ou um código padrão 'default' se não achar
        return codigos.get(nome_clube)
    
    
    def descritivas(self, torneio = 'br'):
        """
        Parameters
        ----------
        torneio : str
            Diretório do arquivo.

        Returns
        -------
        None.

        """
        if torneio == 'br':
            arq = self.caminhos.get(torneio) + "TabelaFinal.xlsx"
            arquivo = pd.read_excel(arq)
            
            # Faz correções ortográficas
            arquivo['TIME'] = Bases.grafia(self, arquivo['TIME'])
            
            t_times = sorted(arquivo['TIME'].unique())
            
            return t_times
        
    
    def diferenca_gols(self, df):
        """
        Calcula a diferença de gols absoluta
        ----------
        df : DataFrame
        Retorna
        -------
        DataFrame.
        """
        df['dif_gols'] = (df['gols_mandante'] - df['gols_visitante']).abs()
        return df        
    
    def grafia(self, coluna):
        """
        Limpeza de colunas.
        ----------
        coluna : object
            Col DataFrame.

        Returns
        -------
        Coluna.

        """
        if not isinstance(coluna, object):
            return coluna
        
        # Espaços adicionais
        #coluna = coluna.strip()
        
        # onde é o H
        coluna = coluna.replace(["Atlético-PR", "Athletico Paranaense"], "Athletico-PR")
        
        coluna = coluna.replace("Atlético Goianiense", "Atlético-GO")
        coluna = coluna.replace("Atlético Mineiro", "Atlético-MG")

        # ' ' FC
        coluna = coluna.replace("Coritiba", "Coritiba FC")
        coluna = coluna.replace("Figueirense", "Figueirense FC")
        coluna = coluna.replace(["Santos", "Santos Fc"], "Santos FC")
        
        # GEC
        coluna = coluna.replace("Bahia", "EC Bahia")
        coluna = coluna.replace("Criciúma", "Criciúma EC")
        coluna = coluna.replace("Goiás", "Goiás EC")
        coluna = coluna.replace(["Fortaleza", "Fortaleza Ec"], "Fortaleza EC")
        coluna = coluna.replace("Vitória", "EC Vitória")

        # SC
        coluna = coluna.replace("Ceará", "Ceará SC")
        coluna = coluna.replace("Paysandu", "Paysandu SC")
        
        # Outros
        coluna = coluna.replace("Cuiabá-MT", "Cuiabá")
        coluna = coluna.replace("Red Bull Bragantino", "RB Bragantino")

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
        
        elif (arquivo.split('.')[-1] == 'xlsx') or (arquivo.split('.')[-1] == 'xls'):
            #print(caminho_cheio)
            try:
                # Tenta ler o arquivo excel
                df = pd.read_excel(caminho_cheio)
                return df
                
            except FileNotFoundError:
                print(caminho_cheio)
                print("Arquivo não encontrado. Por favor, certifique-se que \
                         o arquivo está na pasta.")
                return pd.DataFrame()
   
            
    def pontuar(self, arq, gol_m='gols_mandante', gol_v='gols_visitante'):
        """
        Parâmetros
        ----------
        arq : DataFrame (pandas)
        gol_m : str
            Coluna de gols do mandante.
        gol_v : str
            Coluna de gols do visitante.

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
       
    
    def video(self, arquivo, torneio = 'br'):
        """
        Reprooduz um vídeo
        ----------
        arquivo : str
            Nome do arquivo (com extensão).
        torneio: str
            Diretório do arquivo.

        Retorna
        -------
        Reprodutor de vídeo.

        """
        if torneio == 'br':
            nome = self.caminhos.get(torneio) + arquivo
            video = open(nome, 'rb')
            video_b = video.read() # bytes?

        return st.video(video_b)
