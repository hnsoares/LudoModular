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
from tkinter.messagebox import showinfo
from tkinter import Menu
from os import sep, path  # para achar arquivos

from jogo import partida
from dados import armazenamentoDados as AD
from dados import baseDados as BD

__all__ = ['cria_menu']

CORES = ['yellow', 'green', 'red', 'blue']
WIDTH = 600
HEIGHT = 400
FORMATO = "%sx%s" % (WIDTH, HEIGHT)

ARQUIVO_LOGO_LUDO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'logo_ludo.png'])

def alterar_crendenciais_bd(root):
    def coletar_e_salvar():
        lista = [e1.get(), e2.get(), e3.get()]
        texto = '\n'.join(lista)
        arquivo = BD.PATH_CREDENCIAIS
        with open(arquivo, 'w+') as f:
            f.write(texto)
        janela.destroy()

    default = ['host_mysql', 'usuario', '']
    if BD.existe_arquivo_credenciais():
        with open(BD.PATH_CREDENCIAIS, 'r') as file:
            default = file.read().split('\n')

    janela = Toplevel(root)
    janela.title = "Configuração Credenciais"
    janela.geometry("300x300")

    e1 = Entry(janela)
    e1.place(x=100, y=50)
    e1.insert(10, default[0])
    Label(janela, text='Host').place(x=50, y=50)

    e2 = Entry(janela)
    e2.place(x=100, y=100)
    e2.insert(10, default[1])
    Label(janela, text='Usuario').place(x=50, y=100)

    e3 = Entry(janela, show="*")
    e3.place(x=100, y=150)
    e3.insert(10, default[2])
    Label(janela, text='Senha').place(x=50, y=150)

    botao_salvar = Button(janela, text='Salvar', command=coletar_e_salvar,
                          width=20)
    botao_salvar.place(x=100, y=200)


def chama_partida_nova(root, escolha):
    """Inicia uma partida nova. Cria o menu quando acabar a partida."""
    if not BD.existe_arquivo_credenciais():
        showinfo("Erro", "Cadastre primeiro as credenciais do banco de dados.")
        return

    if escolha.isdigit():
        escolha = int(escolha)
        root.destroy()
        print("Iniciando partida.")
        partida.inicia_partida(CORES[:escolha])
        cria_menu()
    else:
        showinfo("Valor invalido", "Selecione uma quantidade de jogadores")


def chama_partida_salva(root):
    """
    Carrega uma partida salva. Cria o menu quando acabar a partida
    Se não houver partida salva, retorna nada.
    """
    if not BD.existe_arquivo_credenciais():
        showinfo("Erro", "Cadastre primeiro as credenciais do banco de dados.")
        return

    if not AD.detecta_partida_completa():
        showinfo("Erro", "Não há partida salva.")
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
    root.resizable(0, 0)
    root.configure(background='grey')

    logo = PhotoImage(file=ARQUIVO_LOGO_LUDO)

    canvas = Canvas(root, width=350,height=160, background='grey', highlightthickness=0)
    canvas.pack()
    canvas.create_image(20,10, anchor=NW, image=logo)

    texto_num_jogadores = Label(root, text='Escolha o número de jogadores: ', background='grey',
                                font=('Arial','15','bold'))

    combo = Combobox(root, width=15, state="readonly", font=('Arial','12','bold'))
    combo['values'] = (2, 3, 4)  # define as escolhas
    combo.current(0)  # deixa a escolha default com o texto
    carregar_button = Button(root, text="Carregar Partida", command=lambda: chama_partida_salva(root), width=20)
    iniciar_button = Button(root, text='Iniciar Partida',
                            command=lambda: chama_partida_nova(root, combo.get()), width=20)

    credenciais_bd = Menu(root)
    credenciais_bd.add_cascade(label='Configurar credenciais', command= lambda: alterar_crendenciais_bd(root))

    texto_num_jogadores.place(x=WIDTH / 2 - 145, y=HEIGHT * 5 / 7 - 75)
    iniciar_button.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7)
    carregar_button.place(x=WIDTH / 2 - 70, y=HEIGHT * 5 / 7 + 40)
    combo.place(x=WIDTH / 2 - 85, y=HEIGHT * 5 / 7 - 40)
    root.config(menu=credenciais_bd)
    root.mainloop()
