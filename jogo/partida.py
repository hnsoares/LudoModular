"""
Modulo Partida
iniciar_tabuleiro()
adicionar_peoes()
acessar_posicao()
reiniciar_peao()
movimentacao_possivel()
mover_peao()

28/09 (Guilherme): Modulo criado
05/10 (Daniel): Recomecando (reescrevendo tudo)
16/10 (Daniel): Jogar novamente
"""


from jogo import dado
from jogo import peao
from jogo import tabuleiro
from dados import baseDados
from dados import armazenamentoDados
# from unittest.mock import Mock

LISTA_CORES = ['yellow', 'green', 'red', 'blue']
peoes_cor = dict()
conexao_bd = None  # conexao com BD a ser feita

# escolher_peao = Mock(return_value=0)


def escolher_peao(lista):
    print("Escolha o peão: ")
    for i, a in enumerate(lista):
        print('(digite %d): id %d' % (i, a))
    x = input('Sua escolha: ')
    while not (x.isdigit() and (0 <= int(x) < len(lista))):
        x = input("Sua escolha: ")
    return int(x)


def criar_partida():
    """
    Inicializa a partida, criando os peoes e jogadores.
    Retorna 0.
    """
    global conexao_bd

    conexao_bd = baseDados.iniciar_conexao()
    peao.limpar_peoes(conexao_bd)
    peoes_cor.clear()
    tabuleiro.iniciar_tabuleiro(conexao_bd, len(LISTA_CORES))  # 4 cores

    for cor in LISTA_CORES:
        peoes_cor[cor] = list()
        for i in range(4):
            peoes_cor[cor].append(peao.criar_peao(conexao_bd, cor))
        tabuleiro.adicionar_peoes(conexao_bd, peoes_cor[cor])

    return 0


def rodada(cor):
    """
    Faz a rodada.
    3 se pode jogar novamente.
    2 se vitoria,
    1 se nao fez nada,
    0 se foi sucesso,
    levanta erro caso erro.
    """
    global conexao_bd

    jogar_novamente = False
    # rodando dado
    valor_dado = dado.jogar_dado()
    if valor_dado == 6:
        jogar_novamente = True
    print("Rodei o dado: %d" % valor_dado)

    # descobrindo os valores possiveis
    lista_peoes = peoes_cor[cor]
    lista_peoes_possiveis = []
    peoes_finalizados = 0
    for p in lista_peoes:
        x = tabuleiro.movimentacao_possivel(conexao_bd, p, valor_dado)
        if x == -1:
            raise Exception("IdNaoExiste")
        if x == 0:
            lista_peoes_possiveis.append(p)
        if x == 2:
            # o peao ja foi finalizado
            peoes_finalizados += 1

    print("Movimentos possiveis: %d" % len(lista_peoes_possiveis))
    if not lista_peoes_possiveis:
        return 1 if not jogar_novamente else 3

    # escolhendo o peao a mover
    i = escolher_peao(lista_peoes_possiveis)
    peao_pra_mover = lista_peoes_possiveis[i]
    print("Escolhido o peao %d" % i)

    # movendo o peao
    posicao_final = tabuleiro.mover_peao(conexao_bd, peao_pra_mover, valor_dado)
    if posicao_final == -1:
        raise Exception("IdNaoExiste2")

    if posicao_final == -2 and peoes_finalizados == 3:  # ja tinha acabado tres e acabou outro agora
        return 2

    print("Peao movido para a posicao %d" % posicao_final)

    # verificar peao comido
    lista_peoes_posicao = tabuleiro.acessar_posicao(conexao_bd, posicao_final)
    if lista_peoes_posicao == 0:  # casa protegida, nao come
        return 0 if not jogar_novamente else 3

    for p in lista_peoes_posicao:
        cor_p = peao.acessar_peao(conexao_bd, p)
        if cor_p == cor:  # se for da mesma cor, esquece
            continue
        else:
            print("Peao comido: %d" % p)
            tabuleiro.reiniciar_peao(conexao_bd, p)  # comeu o peao
            jogar_novamente = True

    if jogar_novamente:
        return 3
    return 0


def cor_da_rodada():
    i = 0
    while True:
        yield LISTA_CORES[i]
        i += 1
        if i == len(LISTA_CORES):
            i = 0


def rodar_partida():
    """Cria e joga uma partida. Retorna 0 ao seu final."""

    print("Criando a partida.")
    criar_partida()

    print("Comecando a partida. ")
    g = cor_da_rodada()
    x = -1
    cor = ''
    while x != 2:
        if x != 3:  # 3 eh quando a pessoa pode jogar de novo
            cor = next(g)
        print("Vez do %s" % cor)
        x = rodada(cor)
        if x == 1:
            print("Voce nao pode jogar nesta rodada.\n")
        else:
            print("Jogada realizada com sucesso. \n")
            temp = input("Deseja salvar a partida? (y/n): ")
            if temp == 'y':
                armazenamentoDados.salvar_partida_completa(conexao_bd)

    print("%s ganhou" % cor)
    return 0


if __name__ == '__main__':
    rodar_partida()
    baseDados.fechar_conexao(conexao_bd)
