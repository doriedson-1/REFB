# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 16:53:52 2025

@author: drnj2
"""

from config import *

fla = bd[bd['time_mandante'] == 'Flamengo']



for i in range(2003, 2023):
    print("\n", i)
    
    aux = fla.loc[(fla['ano_campeonato'] == i)] #& (fla['data'] < str(i) + '-12-25')]
    
    print(aux.shape)


# OS DADOS DE 2003 e 2004 ESTÃO INCOMPLETOS!
