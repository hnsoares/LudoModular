from random import *
from Jogo.tabuleiro import cria_tabuleiro
__all__ = ['cria_partida']


def lista_jogadores():
    n = int(input("Quantas pessoas irão jogar?\n"))
    lista = []
    for i in range(n):
        nome = input("nome: ")
        lista.append(nome)
    return lista


def define_ordem_jogadores(lista_jogadores):
    return shuffle(lista_jogadores)


def testa_partida(partida):
    '''
    Testa se a partida é realmente uma partida
    '''
    try:
        partida['lista_jogadores']
        partida['tabuleiro']
        partida['ranking']
        partida['turno']
    except KeyError:
        return 0
    return 1


def cria_partida(partida): #recebe uma partida(dict)
    '''
    Retorna um dict com lista de jogadores, tabuleiro,
    lista do ranking, e o turno
    '''
    if testa_partida(partida) == 1:
        pass
    else:
        jogadores = lista_jogadores()
        dict_partida = {
            "lista_jogadores": jogadores,
            "tabuleiro": cria_tabuleiro(len(jogadores)),
            "ranking": [-1, -1, -1, -1],
            "turno": 0
        }
        return dict_partida
