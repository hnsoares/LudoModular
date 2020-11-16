"""
Modulo para a interface grafica do menu.
Sua funcao eh gerenciar a interface inicial, e criar a partida.

Funcoes:
    chama_partida_nova()
    chama_partida_salva()
    fechar_jogo()
    cria_menu()

Feita por Marcos
"""

from tkinter import *
from tkinter.ttk import *

from jogo import partida
from dados import armazenamentoDados as AD

__all__ = ['cria_menu']

CORES = ['yellow', 'green', 'red', 'blue']
WIDTH = 600
HEIGHT = 400
FORMATO = "%sx%s" % (WIDTH, HEIGHT)


def chama_partida_nova(root, escolha):
    """Inicia uma partida nova. Cria o menu quando acabar a partida."""
    if escolha.isdigit():
        escolha = int(escolha)
        root.destroy()
        print("Iniciando partida.")
        partida.inicia_partida(CORES[:escolha])
        cria_menu()
    else:
        print('Valor inválido!')


def chama_partida_salva(root):
    """
    Carrega uma partida salva. Cria o menu quando acabar a partida
    Se não houver partida salva, retorna nada.
    """
    if not AD.detecta_partida_completa():
        print("Nao ha partida salva.")
        return
    root.destroy()
    print("Iniciando partida.")
    partida.inicia_partida([])
    cria_menu()


def fechar_jogo():
    """Fecha o jogo."""
    exit(1)


def cria_menu():
    """Cria o menu com os botoes."""
    root = Tk()  # cria o elemento root
    root.geometry(FORMATO)
    root.title('LUDO')
    combo = Combobox(root, width=29)
    combo['values'] = ('Escolha o número de jogadores', 2, 3, 4)  # define as escolhas
    combo.current(0)  # deixa a escolha default com o texto
    carregar_button = Button(root, text="Carregar Partida", command=lambda: chama_partida_salva(root), width=20)
    iniciar_button = Button(root, text='Iniciar Partida',
                            command=lambda: chama_partida_nova(root, combo.get()), width=20)
    fechar = Button(root, text='Fechar', command=fechar_jogo, width=20)

    iniciar_button.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 - 60)
    carregar_button.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 - 10)
    fechar.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 + 30)
    combo.place(x=WIDTH / 2 - 100, y=HEIGHT * 5 / 7 - 100)
    root.mainloop()
