from Jogador.jogador import *
from tabuleiro import *
from random import *


def define_ordem_jogadores(lista_jogadores):
    shuffle(lista_jogadores)
def cria_partida():
    n=set.numerojogadores()
    for n in range(0,n-1):
        nome=set_nome() #CRIAR SET_NOME
        jogadores.append=jogador.cria_jogador(-1,nome)
    tabuleiro.criar_tabuleiro(n)
    return


