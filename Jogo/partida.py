from random import *
from Jogo.tabuleiro import cria_tabuleiro
__all__ = ['cria_partida']


def lista_jogadores():
    n = int(input("Jog?\n"))
    lista = []
    for i in range(n):
        nome = input("nome: ")
        lista.append(nome)
    return lista


def define_ordem_jogadores(lista_jogadores):
    return shuffle(lista_jogadores)


def testa_partida(partida):
    try:
        partida['lista_jogadores']
        partida['tabuleiro']
        partida['ranking']
        partida['turno']
    except KeyError:
        return 0
    return 1


def cria_partida(partida):
    if testa_partida(partida) == 1:
        pass
    else:
        jogadores = lista_jogadores()
        lista_partida = {
            "lista_jogadores": jogadores,
            "tabuleiro": cria_tabuleiro(len(jogadores)),
            "ranking": [-1, -1, -1, -1],
            "turno": 0
        }
        return lista_partida
