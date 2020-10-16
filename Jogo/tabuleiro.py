__all__ = ["cria_tabuleiro", "altera_tabuleiro"]
import Jogo.peca
import Jogo.casa
specials = [40, 48, 53, 61, 66, 74, 79, 67]


def criar_pecas(numero_jog):
    i = 0
    j = 0
    k = 0
    list_peca = []
    while i < (4*numero_jog):
        pec = Jogo.peca.cria_peca(i, k)
        list_peca.append(pec)
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
            cas = Jogo.casa.cria_casa(i, k, True)
        else:
            cas = Jogo.casa.cria_casa(i, k, False)
        list_casa.append(cas)
        j += 1
        if j % 23 == 0:
            j = 0
            k += 1
        i += 1
    return list_casa


def cria_tabuleiro(numero_jog):  # numero_jog é um int
    '''
    --> Recebe o numero de jogadores e a lista de pos
    <-- Retorna a lista de posições
    '''

    lista_pos = []
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
    return lista_pos


def altera_tabuleiro(lista, uid, numero):
    '''
    Recebe lista de posições , id da peça, e numero de casas que deseja se mover
    '''
    i = 0
    j = 0
    while i < len(lista):
        while j < len(lista[i]['pecas']):
            if lista[i]['pecas'][j]['uid'] == uid:
                casa = lista[i]['pecas'][j]
                lista[i+numero]['pecas'].append(casa)
                del lista[i]['pecas'][j]
                return 0 #Retorna 0 caso o processo tenha sido possível ser realizado
            j += 1
        i += 1
    return 1 #Retorna 1 caso não encontre a peça desejada
