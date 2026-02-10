import streamlit as st
#from recursos import Bases

#bases = Bases()

def chave_confronto(arquivo="C:\\REFB\\_lixo\\teste.html"):
    """
    Parameters
    ----------
    arquivo : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    return st.html(arquivo)

chave_confronto()