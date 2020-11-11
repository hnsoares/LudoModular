import pygame
from os import sep, path
from dados import baseDados

TAMANHO_TELA = ALTURA_TELA, COMPRIMENTO_TELA = (1280, 720)
COR_PRETO = (0, 0, 0)
COR_DEFAULT = (255, 255, 255)
CORES = {'yellow': (255, 255, 0), 'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0)}
ARQUIVO_MUSICA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'musica.wav'])
RAIO = 24
screen = None  # tela a ser configurada
dict_peoes = {}
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


def find_pos(pos):
    if 0 <= pos <= 4:
        return ()


def inicializar(c):
    global screen, dict_peoes
    pygame.init()
    screen = pygame.display.set_mode(TAMANHO_TELA)
    pygame.display.set_caption("Ludo")

    pygame.mixer.music.load(ARQUIVO_MUSICA)
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(loops=True, fade_ms=1000)

    dict_peoes = coletar_todos_peoes(c)


def checa_eventos():
    """
    0 -> 0
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


def coletar_todos_peoes(c):
    p = baseDados.TABELA_PEOES
    t = baseDados.TABELA_TABULEIRO
    cursor = c.cursor(dictionary=True)
    q = "SELECT %s.id, cor, pos from %s inner join %s on %s.id=%s.id" % (p, p, t, p, t)
    cursor.execute(q)
    r = dict()
    for f in cursor.fetchall():
        r[int(f['id'])] = [f['cor'], int(f['pos'])]
    cursor.close()
    return r


def desenha_peao(cor, pos, destacar=False):
    if pos not in dict_posicoes:
        print("ERRO DE POSICAO: ", pos)
        return

    x, y = dict_posicoes[pos]
    x += 280
    if cor not in CORES:
        c = COR_DEFAULT
    else:
        c = CORES[cor]

    pygame.draw.circle(screen, c, (x, y), RAIO)
    if destacar:
        pygame.draw.circle(screen, COR_DEFAULT, (x, y), RAIO, width=RAIO//4)


def atualiza_peao(c, i):
    p = baseDados.selecionar_tabuleiro(c, peao=i)
    dict_peoes[i][1] = p['pos']


def atualiza_tela(c, peoes=None, destacar=None):
    screen.fill(COR_PRETO)

    if peoes is not None:
        for p in peoes:
            atualiza_peao(c, p)

    for p in dict_peoes:
        peao = dict_peoes[p]
        if destacar is not None:
            desenha_peao(peao[0], peao[1], p in destacar)
        else:
            desenha_peao(peao[0], peao[1])

    pygame.display.flip()


def escolhe_peao(c, lista):
    posicoes_lista = [dict_posicoes[baseDados.selecionar_tabuleiro(c, peao=x)['pos']] for x in lista]
    while True:
        pos = checa_eventos()
        if pos is not None:
            x, y = pos
            for i, pos1 in enumerate(posicoes_lista):
                x1, y1 = pos1
                x1 += 280  # offset do canto da tela
                dist = (x - x1)**2 + (y - y1)**2
                # print(dist, x, y, x1, y1)
                if dist <= RAIO**2:
                    return i


# if __name__ == '__main__':
# c = baseDados.iniciar_conexao()
# inicializar(c)
# while True:
# checa_eventos()
# atualiza_tela()
