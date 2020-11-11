"""
Main da build #3
"""
# import tkinter
# from display.menu import cria_menu
# cria_menu()

from jogo import partida

LISTA_CORES = ['yellow', 'green', 'red', 'blue']


def main():
    a = int(input("Digite uma quantidade de jogadores, ou 0 para puxar uma antiga: "))
    partida.inicia_partida(LISTA_CORES[:a])


if __name__ == '__main__':
    main()
