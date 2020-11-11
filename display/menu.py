from tkinter import *
from tkinter.ttk import *
from jogo.partida import rodar_partida

__all__ = ['cria_menu']

def testa_numero(root, num):
    if num != 'Escolha o número de jogadores':
        root.destroy()
        rodar_partida()
    else:
        print('Valor inválido!')

def fechar_jogo():
    exit(1)

def cria_menu():
    root = Tk()
    WIDTH = 600
    HEIGHT = 400
    format = str(WIDTH) + 'x' + str(HEIGHT)
    root.geometry(format)
    root.title('LUDO')
    combo = Combobox(root, width=29)
    combo['values'] = ('Escolha o número de jogadores', 2, 3, 4)
    combo.current(0)
    iniciar_button = Button(root, text='Iniciar', command= lambda : testa_numero(root, combo.get()), width=20)
    fechar = Button(root, text='Fechar', command=fechar_jogo, width=20)

    iniciar_button.place(x=WIDTH/2 - 70, y=HEIGHT*5/7 - 30)
    fechar.place(x=WIDTH/2 - 70, y=HEIGHT*5/7 + 30)
    combo.place(x=WIDTH/2 - 100, y=HEIGHT*5/7 - 100)
    root.mainloop()
