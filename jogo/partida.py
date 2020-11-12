"""
Modulo Partida

Feito por Daniel
"""

from jogo import dado
from jogo import peao
from jogo import tabuleiro
from dados import baseDados
from dados import armazenamentoDados
import datetime
from display import jogo

peoes_cor = dict()
conexao_bd = None  # conexao com BD a ser feita
peoes_atualizar_grafico = []


def _criar_partida(cores):
    """
    Cria uma partida. Retorna os seus dados.
    """
    global conexao_bd
    if conexao_bd is None:
        conexao_bd = baseDados.iniciar_conexao()
    peao.limpar_peoes(conexao_bd)
    tabuleiro.limpar_tabuleiro(conexao_bd)
    peoes_cor.clear()
    tabuleiro.configurar_tabuleiro(len(cores))

    for cor in cores:
        temp = []
        for i in range(4):
            temp.append(peao.criar_peao(conexao_bd, cor))
        tabuleiro.adicionar_peoes(conexao_bd, temp)

    dados = {'hora_criacao': datetime.datetime.now().isoformat(),
             'tempo': '0:0',
             'cores': cores,
             'jogadores': len(cores)}

    return dados


def _carrega_partida():
    """Carrega uma partida. Retorna seus dados, ou -1 se nao havia partida anterior."""
    global conexao_bd
    if conexao_bd is None:
        conexao_bd = baseDados.iniciar_conexao()
    peao.limpar_peoes(conexao_bd)
    tabuleiro.limpar_tabuleiro(conexao_bd)

    dados = armazenamentoDados.recupera_partida_completa(conexao_bd)
    if dados is None:
        return -1

    tabuleiro.configurar_tabuleiro((dados['jogadores']))

    return dados


def _rodada(cor):
    """
    Faz a _rodada.
    3 se pode jogar novamente.
    2 se vitoria,
    1 se nao fez nada,
    0 se foi sucesso,
    levanta erro caso erro.
    """
    global conexao_bd, peoes_atualizar_grafico

    peoes_atualizar_grafico.clear()
    jogar_novamente = False
    # rodando dado
    valor_dado = dado.jogar_dado()
    if valor_dado == 6:
        jogar_novamente = True
    print("Rodei o dado: %d" % valor_dado)

    # descobrindo os valores possiveis
    # lista_peoes = peoes_cor[cor]
    lista_peoes = peao.acessar_peao(conexao_bd, cor=cor)

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

    if peoes_finalizados == 4:
        return 2  # se o cara ja tiver ganhado, manda que ja ganhou, por garantia

    print("Movimentos possiveis: %d" % len(lista_peoes_possiveis))
    if not lista_peoes_possiveis:
        return 1 if not jogar_novamente else 3

    # escolhendo o peao a mover
    # i = escolher_peao(lista_peoes_possiveis)
    print(lista_peoes_possiveis)
    jogo.atualiza_tela(conexao_bd, destacar=lista_peoes_possiveis)
    i = jogo.escolhe_peao(conexao_bd, lista_peoes_possiveis)
    peao_pra_mover = lista_peoes_possiveis[i]
    print("Escolhido o peao %d" % i)
    peoes_atualizar_grafico.append(peao_pra_mover)

    # movendo o peao
    posicao_final = tabuleiro.mover_peao(conexao_bd, peao_pra_mover, valor_dado)
    if posicao_final == -1:
        raise Exception("IdNaoExiste2")

    if posicao_final == -2:
        if peoes_finalizados == 3:  # ja tinha acabado tres e acabou outro agora
            return 2
        print("Voce chegou ate o final com seu peao!")
        return 3  # pode jogar de novo

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
            peoes_atualizar_grafico.append(p)
            jogar_novamente = True

    if jogar_novamente:
        return 3
    return 0


def _rodar_partida(dados):
    """Joga uma partida. Retorna 0 ao seu final."""

    cores = dados['cores']
    minutos, segundos = dados['tempo'].split(':')
    tempo_decorrido_inicial = int(minutos) * 60 + int(segundos)
    hora_inicial = datetime.datetime.now()

    while cores:
        cor = cores.pop(0)
        print("Vez do %s" % cor)
        jogo.atualiza_tela(conexao_bd, peoes_atualizar_grafico)
        x = _rodada(cor)
        if x == 2:
            print("Voce ganhou!")
            continue  # a cor nao volta pra lista de cores
        if x == 1:
            print("Voce nao pode realizar nenhum movimento.")

        print("Rodada finalizada.\n")
        if x == 3:
            cores.insert(0, cor)
        else:
            cores.append(cor)

        tempo_decorrido = (datetime.datetime.now() - hora_inicial).total_seconds() + tempo_decorrido_inicial
        dados['tempo'] = "%d:%d" % (tempo_decorrido // 60, tempo_decorrido % 60)

        armazenamentoDados.salvar_partida_completa(conexao_bd, dados)

    return 0


def inicia_partida(lista_cores):
    """
    Inicia uma partida.
    Recebe as cores da partida e a cria.
    Se for uma lista vazia, recupera uma partida antiga.
        Se nao tiver partida, retorna erro.
    E depois, roda.
    """
    global conexao_bd
    conexao_bd = baseDados.iniciar_conexao()

    print("Criando/Carregando a partida.")
    if len(lista_cores) == 0:
        dados = _carrega_partida()
    else:
        dados = _criar_partida(lista_cores)

    print("Iniciando a partida criada em %s, jogada por %s minutos" % (dados['hora_criacao'], dados['tempo']))
    jogo.inicializar(conexao_bd)
    _rodar_partida(dados)
    baseDados.fechar_conexao(conexao_bd)
    print("Fechando conexao.")
    return
