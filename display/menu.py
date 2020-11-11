from tkinter import *
from tkinter.ttk import *

from jogo import partida

__all__ = ['cria_menu']

CORES = ['yellow', 'green', 'blue', 'red']
WIDTH = 600
HEIGHT = 400
FORMATO = "%sx%s" % (WIDTH, HEIGHT)


def testa_numero(root, escolha):
    if type(escolha) == int or escolha.isdigit():
        escolha = int(escolha)
        root.destroy()
        partida.inicia_partida(CORES[:escolha])
        cria_menu()
    else:
        print('Valor inválido!')


def fechar_jogo():
    exit(1)


def cria_menu():
    root = Tk()
    root.geometry(FORMATO)
    root.title('LUDO')
    combo = Combobox(root, width=29)
    combo['values'] = ('Escolha o número de jogadores', 2, 3, 4)
    combo.current(0)
    carregar_button = Button(root, text="Carregar Partida", command=lambda: testa_numero(root, 0), width=20)
    iniciar_button = Button(root, text='Iniciar Partida', command=lambda: testa_numero(root, combo.get()), width=20)
    fechar = Button(root, text='Fechar', command=fechar_jogo, width=20)

    iniciar_button.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 - 60)
    carregar_button.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 - 10)
    fechar.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 + 30)
    combo.place(x=WIDTH / 2 - 100, y=HEIGHT * 5 / 7 - 100)
    root.mainloop()
