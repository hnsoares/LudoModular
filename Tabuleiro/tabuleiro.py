__all__ = ["cria_tabuleiro"]
from Peca.peca import *
from Casa.casa import *
specials = [48, 61, 74, 67]


def criar_pecas(numero_jog):
    i = 0
    j = 0
    k = 0
    list_peca = []
    while i < (4*numero_jog):

        peca = cria_peca(i, k)
        list_peca.append(peca)
        j += 1
        if j % 4 == 0:
            j = 0
            k += 1
        i += 1
    return list_peca


def criar_casas():

    i = 0
    j = 0
    k = 0
    list_casa = []
    while i < (92):

        if i in specials:
            casa = cria_casa(i, k, True)
        else:
            casa = cria_casa(i, k, False)
        list_casa.append(casa)
        j += 1
        if j % 23 == 0:
            j = 0
            k += 1
        i += 1
    return list_casa


def cria_tabuleiro(numero_jog, lista_pos):  # numero_jog é um int e lista_pos é um array
    '''
    --> Recebe o numero de jogadores e a lista de pos
    <-- Retorna 1 se foi possivel criar a lista 
    e 0 se ocorreu algum erro
    '''
    if numero_jog > 4:
        return 0
    list_casa = criar_casas()
    for i in range(len(list_casa)):
        item = {
            "posicao": list_casa[i]["uid"],
            "casa": list_casa[i],
            "pecas": []
        }
        lista_pos.append(item)
    list_peca = criar_pecas(numero_jog)
    for i in range(len(list_peca)):
        lista_pos[i]["pecas"].append(list_peca[i])
    return 1
