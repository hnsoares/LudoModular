"""
Modulo para a interface grafica do jogo (partida).
Sua funcao eh gerenciar a interface, e respondendo suas interações.

Funcoes:
    inicializar(c)
    escolhe_peao(c, lista)
    atualiza_tela(c, [peoes], [destacar])
    fechar()

Feita por Daniel
"""

import pygame
from os import sep, path  # para achar arquivos
from dados import baseDados
from json import load

TAMANHO_TELA = COMPRIMENTO_TELA, ALTURA_TELA = (1280, 720)  # por enquanto, se trocar, da ruim
COR_PRETO = (0, 0, 0)
COR_DEFAULT = (255, 255, 255)  # branco
CORES = {'yellow': (255, 255, 0), 'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0)}
RAIO_CIRCULO = 24

POS_BOTAO = 20, 20

ARQUIVO_MUSICA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'musica.wav'])
ARQUIVO_FUNDO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'tabuleiro720.png'])
ARQUIVO_POSICOES = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'posicoes.json'])
ARQUIVO_SOM_PECA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'peca.wav'])
ARQUIVO_SOM_CAPTURA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'captura.wav'])
ARQUIVO_SOM_VITORIA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'vitoria.wav'])
ARQUIVO_SOM_DADO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado.wav'])
ARQUIVO_BOTAO_MUSICA_ON = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bmusica_on.png'])
ARQUIVO_BOTAO_MUSICA_OFF = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bmusica_off.png'])
ARQUIVO_BOTAO_SOM_ON = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bsom_on.png'])
ARQUIVO_BOTAO_SOM_OFF = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bsom_off.png'])


screen = None  # tela a ser configurada
imagem_fundo = None  # imagem de fundo que vai ser carregada
rect_imagem_fundo = None  # objeto da image de fundo que vai ser carregada
dict_peoes = {}  # dicionario para guardar os peoes (cache)
dict_posicoes = None  # dicionario para posicoes (gerado no inicializar)

font_texto = None
texto_exemplo = None

bool_tocar_som = True
som_peca = None
som_captura = None
som_vitoria = None
som_dado = None

bool_tocar_musica = True
botao_musica_on = None
botao_musica_off = None
rect_botao_musica = None
botao_som_on = None
botao_som_off = None
rect_botao_som = None


def inicializar(c):
    """
    Inicializa a interface grafica:
        Abre a tela do jogo.
        Inicia a musica.
        Carrega o fundo.
        Carrega posicoes
    Retorna nada.
    """
    global screen, imagem_fundo, rect_imagem_fundo, dict_posicoes
    global font_texto, texto_exemplo
    global som_peca, som_captura, som_vitoria, som_dado
    global botao_musica_on, rect_botao_musica, botao_musica_off
    global botao_som_on, botao_som_off, rect_botao_som

    print("Iniciando pygame: ", end='')

    pygame.init()
    screen = pygame.display.set_mode(TAMANHO_TELA)
    pygame.display.set_caption("Ludo")

    # MUSICA
    pygame.mixer.music.load(ARQUIVO_MUSICA)
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(loops=True, fade_ms=1000)

    # SOM
    som_peca = pygame.mixer.Sound(ARQUIVO_SOM_PECA)
    som_captura = pygame.mixer.Sound(ARQUIVO_SOM_CAPTURA)
    som_vitoria = pygame.mixer.Sound(ARQUIVO_SOM_VITORIA)
    som_dado = pygame.mixer.Sound(ARQUIVO_SOM_DADO)

    # BOTOES
    botao_musica_on = pygame.image.load(ARQUIVO_BOTAO_MUSICA_ON)
    rect_botao_musica = botao_musica_on.get_rect()
    rect_botao_musica.x, rect_botao_musica.y = POS_BOTAO
    botao_musica_off = pygame.image.load(ARQUIVO_BOTAO_MUSICA_OFF)

    botao_som_on = pygame.image.load(ARQUIVO_BOTAO_SOM_ON)
    rect_botao_som = botao_som_on.get_rect()
    rect_botao_som.x, rect_botao_som.y = POS_BOTAO[0], POS_BOTAO[1] + 50 + 20
    botao_som_off = pygame.image.load(ARQUIVO_BOTAO_SOM_OFF)

    # FUNDO
    imagem_fundo = pygame.image.load(ARQUIVO_FUNDO)
    rect_imagem_fundo = imagem_fundo.get_rect()
    rect_imagem_fundo.x = (COMPRIMENTO_TELA - ALTURA_TELA) // 2  # posiciona no centro
    rect_imagem_fundo.y = 0

    # POSICOES
    with open(ARQUIVO_POSICOES, 'r') as f:
        # o arquivo esta como 'str': [int, int]. Mas eu quero int: [int, int]
        # por isso, vou converter para inteiro todas as chaves
        # lambda vai ser uma funcao que recebe o dic, e retorna faz um dict comprehension
        # que pega a chave, transforma em int, e atribui ao conteudo, pego atraves de dict.items()
        dict_posicoes = load(f, object_hook=lambda d: {int(a): b for a, b in d.items()})
    print("DONE")

    print("Carrengando peoes: ", end="")
    _monta_cache_peoes(c)
    print("DONE")

    # TEXTOS
    font_texto = pygame.font.SysFont('bahnschrift.ttf', 24)
    texto_exemplo = font_texto.render('F3/F4 -> Pausa/Continua musica', True, COR_DEFAULT)


def _checa_eventos():
    """
    Verifica a interacao com a interface grafica.
    Se o jogo fechar, ele fecha sem salvar.
    F3 e F4 pausam e continuam a musica.
    Retorna a posicao do mouse se houver algum clique.
    Senao, retorna nada.
    """
    global bool_tocar_musica, bool_tocar_som

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fechar()
            exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if POS_BOTAO[0] <= x <= POS_BOTAO[0] + 50 and (POS_BOTAO[1] <= y <= POS_BOTAO[1] + 50):
                bool_tocar_musica = not bool_tocar_musica
                if bool_tocar_musica:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                atualiza_tela(travar_destaque=True)  # ja que mudou na tela

            elif POS_BOTAO[0] <= x <= POS_BOTAO[0] + 50 and POS_BOTAO[1] + 50 + 20 <= y <= POS_BOTAO[1] + 50 + 50 + 20:
                bool_tocar_som = not bool_tocar_som
                atualiza_tela(travar_destaque=True)  # ja que mudou na tela

            return x, y
    return


def _monta_cache_peoes(c):
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
        dict_peoes[int(f['id'])] = [f['cor'], int(f['pos']), False]  # dicionario para o cache interno
        # o terceiro termo diz se o peao esta destacado ou nao
    cursor.close()
    return


def _desenha_peao(cor, pos, destacar=False):
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


def _atualiza_peao(c, i):
    """Recebe um id, e atualiza o cache interno."""
    p = baseDados.selecionar_tabuleiro(c, peao=i)
    dict_peoes[i][1] = p['pos']


def atualiza_tela(c=None, atualizar=None, destacar=None, travar_destaque=False):
    """
    Atualiza a tela da interface do jogo.
    Se atualizar for uma lista de ids:
        Esses peoes serao atualizados
        Precis da conexao com a base de dados
    Se destacar for uma lista de ids:
        Esses peoes serao destacados.
    Se travar_destaque, os destaques nao seram excluidos
    """

    screen.fill(COR_PRETO)  # fundo preto
    screen.blit(imagem_fundo, rect_imagem_fundo)  # imagem de fundo
    if bool_tocar_musica:
        screen.blit(botao_musica_on, rect_botao_musica)
    else:
        screen.blit(botao_musica_off, rect_botao_musica)

    if bool_tocar_som:
        screen.blit(botao_som_on, rect_botao_som)
    else:
        screen.blit(botao_som_off, rect_botao_som)

    if atualizar is not None:  # atualiza os peoes no cache
        for p in atualizar:
            _atualiza_peao(c, p)

    if destacar is not None:  # destaca os peoes
        for p in destacar:
            dict_peoes[p][2] = True

    for p in dict_peoes:  # desenha todos os peoes.
        peao = dict_peoes[p]
        _desenha_peao(peao[0], peao[1], peao[2])

        if destacar is not None:
            if p not in destacar:
                dict_peoes[p][2] = False
        elif not travar_destaque:
            dict_peoes[p][2] = False

    # texto_exemplo_rect = texto_exemplo.get_rect()
    # texto_exemplo_rect.x, texto_exemplo_rect.y = 0, 0
    # screen.blit(texto_exemplo, texto_exemplo_rect)

    pygame.display.flip()  # atualiza a tela
    pygame.time.wait(100)  # espera 100ms


def escolhe_peao(c, lista):
    """
    Retorna o indice do peao selecionado na lista fornecida.
    Fica nessa funcao ate o jogador selecionar algum peao.
    """
    # lista de posicoes de cada peao
    posicoes_lista = [dict_posicoes[baseDados.selecionar_tabuleiro(c, peao=x)['pos']] for x in lista]
    while True:
        pos = _checa_eventos()
        if pos is not None:  # o mouse foi clicado
            x, y = pos  # posicao do mouse
            for i, pos1 in enumerate(posicoes_lista):
                x1, y1 = pos1  # posicao do peao
                x1 += 280  # offset do canto da tela (deve ser corrigido se alterar as posicoes
                dist = (x - x1) ** 2 + (
                            y - y1) ** 2  # distancia do clique do mouse deve ser menor que o raio do circulo
                # print(dist, x, y, x1, y1)
                if dist <= RAIO_CIRCULO ** 2:
                    return i


def toca_som(som):
    """
    Toca o som se ele estiver ligado.
    0 -> Peça
    1 -> Dado
    2 -> Captura
    3 -> Vitoria


    Não retorna nada.
    """
    global som_peca, som_captura, som_dado, som_vitoria

    if not bool_tocar_som:
        return

    if som == 0:
        som_peca.play()

    elif som == 1:
        som_dado.play()

    elif som == 2:
        som_captura.play()

    elif som == 3:
        som_vitoria.play()

    return


def fechar():
    print("Fechando o jogo")
    pygame.quit()
