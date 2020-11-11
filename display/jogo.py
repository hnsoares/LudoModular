"""
Modulo para a interface grafica do jogo (partida).
Sua funcao eh gerenciar a interface, e respondendo suas interações.

Funcoes:
    inicializar(c)
    escolhe_peao(c, lista)
    atualiza_tela(c, [peoes], [destacar])

Feita por Daniel
"""

import pygame
from os import sep, path  # para achar arquivos
from dados import baseDados

TAMANHO_TELA = COMPRIMENTO_TELA, ALTURA_TELA = (1280, 720)  # por enquanto, se trocar, da ruim
COR_PRETO = (0, 0, 0)
COR_DEFAULT = (255, 255, 255)  # branco
CORES = {'yellow': (255, 255, 0), 'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0)}
RAIO_CIRCULO = 24

ARQUIVO_MUSICA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'musica.wav'])
ARQUIVO_FUNDO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'tabuleiro720.png'])

screen = None  # tela a ser configurada
imagem_fundo = None  # imagem de fundo que vai ser carregada
rect_imagem_fundo = None  # objeto da image de fundo que vai ser carregada
dict_peoes = {}  # dicionario para guardar os peoes (cache)
dict_posicoes = {0: (312, 648),
                 1: (312, 600),
                 2: (312, 552),
                 3: (312, 504),
                 4: (312, 456),
                 5: (264, 408),
                 6: (216, 408),
                 7: (168, 408),
                 8: (120, 408),
                 9: (72, 408),
                 10: (24, 408),
                 11: (24, 360),
                 12: (24, 312),
                 13: (72, 312),
                 14: (120, 312),
                 15: (168, 312),
                 16: (216, 312),
                 17: (264, 312),
                 18: (312, 264),
                 19: (312, 216),
                 20: (312, 168),
                 21: (312, 120),
                 22: (312, 72),
                 23: (312, 24),
                 24: (360, 24),
                 25: (408, 24),
                 26: (405, 72),
                 27: (405, 120),
                 28: (405, 168),
                 29: (405, 216),
                 30: (405, 268),
                 31: (456, 312),
                 32: (504, 312),
                 33: (552, 312),
                 34: (600, 312),
                 35: (648, 312),
                 36: (696, 312),
                 37: (696, 360),
                 38: (696, 408),
                 39: (648, 408),
                 40: (648, 408),
                 41: (552, 408),
                 42: (504, 408),
                 43: (456, 408),
                 44: (408, 456),
                 45: (408, 504),
                 46: (408, 552),
                 47: (408, 600),
                 48: (408, 648),
                 49: (408, 696),
                 50: (360, 696),
                 51: (312, 696),
                 100: (120, 552),
                 101: (168, 600),
                 102: (120, 648),
                 103: (72, 600),
                 200: (120, 72),
                 201: (168, 120),
                 202: (120, 168),
                 203: (72, 120),
                 300: (600, 72),
                 301: (648, 120),
                 302: (600, 168),
                 303: (552, 120),
                 400: (600, 552),
                 401: (648, 600),
                 402: (600, 648),
                 403: (552, 600),
                 1000: (360, 648),
                 1001: (360, 600),
                 1002: (360, 552),
                 1003: (360, 504),
                 1004: (360, 456),
                 1005: (360, 408),
                 2000: (72, 360),
                 2001: (120, 360),
                 2002: (168, 360),
                 2003: (216, 360),
                 2004: (264, 360),
                 2005: (312, 360),
                 3000: (360, 72),
                 3001: (360, 120),
                 3002: (360, 168),
                 3003: (360, 216),
                 3004: (360, 264),
                 3005: (360, 312),
                 4000: (648, 360),
                 4001: (600, 360),
                 4002: (552, 360),
                 4003: (504, 360),
                 4004: (456, 360),
                 4005: (408, 360)}


def inicializar(c):
    """
    Inicializa a interface grafica:
        Abre a tela do jogo.
        Inicia a musica.
        Carrega o fundo.
    Retorna nada.
    """
    global screen, imagem_fundo, rect_imagem_fundo
    pygame.init()
    screen = pygame.display.set_mode(TAMANHO_TELA)
    pygame.display.set_caption("Ludo")

    # MUSICA
    pygame.mixer.music.load(ARQUIVO_MUSICA)
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(loops=True, fade_ms=1000)

    # FUNDO
    imagem_fundo = pygame.image.load(ARQUIVO_FUNDO)
    rect_imagem_fundo = imagem_fundo.get_rect()
    rect_imagem_fundo.x = (COMPRIMENTO_TELA - ALTURA_TELA) // 2  # posiciona no centro
    rect_imagem_fundo.y = 0

    monta_cache_peoes(c)


def checa_eventos():
    """
    Verifica a interacao com a interface grafica.
    Se o jogo fechar, ele fecha sem salvar.
    F3 e F4 pausam e continuam a musica.
    Retorna a posicao do mouse se houver algum clique.
    Senao, retorna nada.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                pygame.mixer.music.pause()
            elif event.key == pygame.K_F4:
                pygame.mixer.music.unpause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos()
    return


def monta_cache_peoes(c):
    """
    Pega todos os peoes e informacoes necessarias para criar um cache interno.
    """
    global dict_peoes

    p = baseDados.TABELA_PEOES
    t = baseDados.TABELA_TABULEIRO
    cursor = c.cursor(dictionary=True)

    # SELECT peoes.id, cor, pos from peoes inner join tabuleiro on peoes.id = tabuleiro.id
    q = "SELECT %s.id, cor, pos from %s inner join %s on %s.id=%s.id" % (p, p, t, p, t)
    cursor.execute(q)

    for f in cursor.fetchall():
        dict_peoes[int(f['id'])] = [f['cor'], int(f['pos'])]  # dicionario para o cache interno
    cursor.close()
    return


def desenha_peao(cor, pos, destacar=False):
    """
    Tenta desenhar um peao na tela.
    Se destacar for True, o peao sera destacado
    Se nao conseguir desenhar, nao desenha.
    """
    if pos not in dict_posicoes:  # acha a posicao
        print("ERRO DE POSICAO: ", pos)
        return

    x, y = dict_posicoes[pos]
    x += 280
    if cor not in CORES:
        c = COR_DEFAULT
    else:
        c = CORES[cor]

    pygame.draw.circle(screen, c, (x, y), RAIO_CIRCULO)
    if destacar:
        pygame.draw.circle(screen, COR_DEFAULT, (x, y), RAIO_CIRCULO, width=RAIO_CIRCULO // 4)


def atualiza_peao(c, i):
    """Recebe um id, e atualiza o cache interno."""
    p = baseDados.selecionar_tabuleiro(c, peao=i)
    dict_peoes[i][1] = p['pos']


def atualiza_tela(c, atualizar=None, destacar=None):
    """
    Atualiza a tela da interface do jogo.
    Se atualizar for uma lista de ids:
        Esses peoes serao atualizados
    Se destacar for uma lista de ids:
        Esses peoes serao destacados.
    """

    screen.fill(COR_PRETO)  # fundo preto
    screen.blit(imagem_fundo, rect_imagem_fundo)  # imagem de fundo

    if atualizar is not None:  # atualiza os peoes no cache
        for p in atualizar:
            atualiza_peao(c, p)

    for p in dict_peoes:  # desenha todos os peoes.
        peao = dict_peoes[p]
        if destacar is not None:  # tem que verificar se aquele peao eh destacavel
            desenha_peao(peao[0], peao[1], p in destacar)  # p in destacar eh true se ele deve ser destacado
        else:
            desenha_peao(peao[0], peao[1])  # se nao, joga tudo como false

    pygame.display.flip()  # atualiza a tela


def escolhe_peao(c, lista):
    """
    Retorna o indice do peao selecionado na lista fornecida.
    Fica nessa funcao ate o jogador selecionar algum peao.
    """
    # lista de posicoes de cada peao
    posicoes_lista = [dict_posicoes[baseDados.selecionar_tabuleiro(c, peao=x)['pos']] for x in lista]
    while True:
        pos = checa_eventos()
        if pos is not None:  # o mouse foi clicado
            x, y = pos  # posicao do mouse
            for i, pos1 in enumerate(posicoes_lista):
                x1, y1 = pos1  # posicao do peao
                x1 += 280  # offset do canto da tela (deve ser corrigido se alterar as posicoes
                dist = (x - x1)**2 + (y - y1)**2  # distancia do clique do mouse deve ser menor que o raio do circulo
                # print(dist, x, y, x1, y1)
                if dist <= RAIO_CIRCULO**2:
                    return i

