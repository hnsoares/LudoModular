"""
Modulo Tabuleiro.
lista_posicao_iniciais
lista_posicao_seguras
lista_posicao_finais
tabela_peoes:
    id <id> -> id dos peoes
    pos <int> -> posicao atual do peao
    pos_inicial <int> -> posicao original do peao
    eh_finalizado <bool> -> se ja foi até o fim
    eh_inicio <bool> -> esta na origem

Esquema da numeracao das casas:
    casas normais: 0 .. 13*n - 1

    # casas iniciais: 100*i + j
    i (jogador): 1 .. n, j: 0 .. m

    casas finais: 1000*n + j
    i (jogador): 1 .. n, j: 0 .. 5 (onde 5 eh a casa final)

    casas seguras: 13*i e 13*i + 8, i: 0 .. 3

05/10 (Daniel): Funcoes de acesso do tabuleiro
06/10 (Daniel): Refatorando pequenos detalhes
11/10 (Daniel): Corrigindo reset do tabuleiro
"""

from dados import baseDados

N_CORES = 4  # definindo o default do numero de jogadores como 4
N_PEOES = 4  # definindo o default do numero de peoes por jogador como 4
ID_CASA_FINAL = 1000  # as casas finais comecam em um multiplo de 1000
ID_CASA_INICIAL = 100  # as casas iniciais comecam em um multiplo de 100
lista_posicao_iniciais = []  # lista de pos do inicio
lista_posicao_seguras = []  # lista de posicoes onde nao se pode comer
lista_posicao_finais = []  # lista de posicoes finais do tabuleiro (ultima casa possivel)
# tabela_peoes = []  # lista para guardar as informacoes do peao
cores_acrescentadas = 0   # contador para adicionar peoes. +1 para cada cor acrescentada.


def _achar_peao(c, id_peao):
    """
    Recebe um id, retorna suas informacoes, -1 se nao existir.
    """
    # for i, p in enumerate(tabela_peoes):
    #     if p['id'] == id_peao:
    #         return i

    return baseDados.selecionar_tabuleiro(c, peao=id_peao)


def _definir_posicoes_iniciais(n, m=N_PEOES):
    """
    Recebe um numero n (ate 9) de jogadores, retorna uma lista de n elementos,
    em que cada elemento eh uma lista das posicoes m das casas iniciais.
    """
    global lista_posicao_iniciais
    lista_posicao_iniciais = [[x * ID_CASA_INICIAL + y for y in range(m)] for x in range(1, n + 1)]
    return


def _definir_posicoes_seguras(n):
    """
    Recebe o numero de jogadores, e salva a lista de posicoes de casas seguras.
    """
    global lista_posicao_seguras
    lista_posicao_seguras.clear()
    for i in range(n):
        lista_posicao_seguras.append(13 * i)
        lista_posicao_seguras.append(13 * i + 8)
    return


def _definir_posicoes_finais(n):
    """
    Recebe o numero de jogadores, e salva a lista das ultimas posicoes (casa final).
    """
    global lista_posicao_finais
    lista_posicao_finais = []
    lista_posicao_finais = [ID_CASA_FINAL * n + 5 for n in range(1, n + 1)]
    return


def iniciar_tabuleiro(c, n=N_CORES):
    """
    Recebe o numero de jogadores, e inicia o tabuleiro. Retorna 0.
    """
    global cores_acrescentadas, N_CORES  # , tabela_peoes
    # tabela_peoes.clear()
    baseDados.limpar_tabuleiro(c)
    _definir_posicoes_iniciais(n)
    _definir_posicoes_seguras(n)
    _definir_posicoes_finais(n)
    cores_acrescentadas = 0
    N_CORES = n
    return 0


def adicionar_peoes(c, lista_ids, lista_posicoes=None):
    """
    Recebe uma lista de peoes e uma lista de posicoes atuais e salva na tabela.
    Retorna 0 se sucesso,
    1 se id repetido,
    2 se lista de posicoes invalida,
    3 se ja foram acrescentadas todas as cores,
    """

    global cores_acrescentadas
    # tamanhos de listas diferentes
    if lista_posicoes is not None and len(lista_ids) != len(lista_posicoes):
        return 2

    # ja acrescentaram todas as cores
    if cores_acrescentadas == N_CORES:
        return 3

    # quantidade de um time diferente de quantidade definida de peoes
    if len(lista_ids) != N_PEOES:
        return 2

    for i, id_peao in enumerate(lista_ids):
        # for p in tabela_peoes:
        #     if id_peao == p['id']:
        #        return 1
        if baseDados.selecionar_tabuleiro(c, id_peao) != -1:
            return 1

        d = dict()
        d['id'] = id_peao
        d['pos_inicial'] = lista_posicao_iniciais[cores_acrescentadas][i]
        if lista_posicoes is not None:
            d['pos'] = lista_posicoes[i]
            d['eh_finalizado'] = lista_posicoes[i] in lista_posicao_finais
            d['eh_inicio'] = lista_posicoes[i] in lista_posicao_iniciais
        else:
            d['pos'] = d['pos_inicial']
            d['eh_finalizado'] = False
            d['eh_inicio'] = True

        # tabela_peoes.append(d)
        baseDados.adicionar_tabuleiro(c, d['id'], d['pos'], d['pos_inicial'], d['eh_inicio'], d['eh_finalizado'])

    cores_acrescentadas += 1

    return 0


def acessar_posicao(c, pos):
    """Retorna uma lista dos ids naquela posicao, 0 se a casa for segura."""
    if pos in lista_posicao_seguras:
        return 0
    # pega o id do x da tabela se x esta na posicao 'pos'
    # return [x['id'] for x in tabela_peoes if x['pos'] == pos]

    return [x['id'] for x in baseDados.selecionar_tabuleiro(c, pos=pos)]


def reiniciar_peao(c, id_peao):
    """
    Realoca o peao para a posicao inicial, reiniciando seus dados.
    0 se sucesso,
    -1 se nao houver esse id.
    """
    # i = _achar_peao(id_peao)
    # if i == -1:
    #    return -1

    p = baseDados.selecionar_tabuleiro(c, peao=id_peao)
    if p == -1:
        return -1

    # p = tabela_peoes[i]
    p['pos'] = p['pos_inicial']
    p['eh_finalizado'] = False
    p['eh_inicio'] = True

    baseDados.modificar_tabuleiro(c, id_peao, p['pos'], p['pos_inicial'], p['eh_inicio'], p['eh_finalizado'])
    return 0


def movimentacao_possivel(c, id_peao, mov):
    """
    Retorna se eh possivel movimentar o peao.
    0 se for possivel,
    1 se impossivel,
    2 se finalizado
    -1 se nao existir esse id.
    """
    # i = _achar_peao(id_peao)
    # if i == -1:
    #    return -1
    # p = tabela_peoes[i]

    p = baseDados.selecionar_tabuleiro(c, peao=id_peao)
    if p == -1:
        return -1

    pos = p['pos']
    eh_inicio = p['eh_inicio']
    eh_finalizado = p['eh_finalizado']

    if eh_finalizado:  # se ele ja acabou o jogo
        return 2

    if eh_inicio:  # se ele esta na base ainda
        return 0 if mov == 6 else 1  # se nao tirou 6, nao pode se mover

    if pos >= 1000:  # se esta nas casas finais
        x = 5 - (pos % 1000)
        return 1 if mov > x else 0  # se mov > quanto falta, nao pode se mover

    # em qualquer outro caso, o peao pode ser movido
    return 0


def mover_peao(c, id_peao, mov):
    """
    Move o peao. Admite-se que a movimentacao ja foi valida. Retorna:
    posicao se o movimento foi feito com sucesso,
    -1 se o id nao existir,
    -2 se o peao chegou na ultima casa.

    OBS: nunca retornara a posicao da ultima casa.
    """

    # i = _achar_peao(id_peao)
    # if i == -1:
    #     return -1
    # p = tabela_peoes[i]

    p = baseDados.selecionar_tabuleiro(c, peao=id_peao)
    if p == -1:
        return -1

    pos = p['pos']
    pos_inicial = p['pos_inicial']
    time = pos_inicial // 100  # diz se o time ("cor") eh 1, 2, 3 ou 4.

    if p['eh_inicio']:  # ele vai colocar na casa de saida
        p['eh_inicio'] = False
        new_pos = 13*(time-1)
        p['pos'] = new_pos
        baseDados.modificar_tabuleiro(c, id_peao, p['pos'], p['pos_inicial'], p['eh_inicio'], p['eh_finalizado'])
        return new_pos

    if pos >= 1000:  # reta final. Confere se o peao finalizou
        new_pos = pos + mov
        p['pos'] = new_pos
        if new_pos % 1000 == 5:
            p['eh_finalizado'] = True
            baseDados.modificar_tabuleiro(c, id_peao, p['pos'], p['pos_inicial'], p['eh_inicio'], p['eh_finalizado'])
            return -2

        baseDados.modificar_tabuleiro(c, id_peao, p['pos'], p['pos_inicial'], p['eh_inicio'], p['eh_finalizado'])
        return new_pos

    # primeiro calcula a casa para entrar na reta final
    casa_entrada = (13*(time-1) + 50) % 52  # primeira casa + 50, dando a volta
    new_pos = (pos + mov)  # primeiro vejo sem dar a volta
    if pos <= casa_entrada < new_pos:  # ele deve entrar na reta final
        new_pos = (new_pos - casa_entrada - 1) + time*1000
    else:
        new_pos = new_pos % 52  # senao, so corrige a posicao

    p['pos'] = new_pos  # salva e retorna

    baseDados.modificar_tabuleiro(c, id_peao, p['pos'], p['pos_inicial'], p['eh_inicio'], p['eh_finalizado'])
    return new_pos
