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
from time import time  # para contagem do tempo

TAMANHO_TELA = COMPRIMENTO_TELA, ALTURA_TELA = (1280, 720)  # por enquanto, se trocar, da ruim
COR_PRETO = (0, 0, 0)
COR_DEFAULT = (255, 255, 255)  # branco
CORES = {'yellow': (255, 255, 0), 'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0),
         'default': COR_DEFAULT, 'black': COR_PRETO}

POS_BOTAO = 20, 20

ARQUIVO_MUSICA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'musica.wav'])
ARQUIVO_FUNDO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'tabuleiro720_2.png'])
ARQUIVO_POSICOES = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'posicoes.json'])
ARQUIVO_SOM_PECA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'peca.wav'])
ARQUIVO_SOM_CAPTURA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'captura.wav'])
ARQUIVO_SOM_VITORIA = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'vitoria.wav'])
ARQUIVO_SOM_DADO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado.wav'])
ARQUIVO_BOTAO_MUSICA_ON = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bmusica_on.png'])
ARQUIVO_BOTAO_MUSICA_OFF = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bmusica_off.png'])
ARQUIVO_BOTAO_SOM_ON = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bsom_on.png'])
ARQUIVO_BOTAO_SOM_OFF = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'bsom_off.png'])
ARQUIVO_PECA_VERDE = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'peca_verde.png'])
ARQUIVO_PECA_AZUL = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'peca_azul.png'])
ARQUIVO_PECA_VERMELHO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'peca_vermelho.png'])
ARQUIVO_PECA_AMARELO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'peca_amarelo.png'])
ARQUIVO_PECA_SELECAO = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'selecao.png'])
ARQUIVO_DADO_1 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado1.png'])
ARQUIVO_DADO_2 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado2.png'])
ARQUIVO_DADO_3 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado3.png'])
ARQUIVO_DADO_4 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado4.png'])
ARQUIVO_DADO_5 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado5.png'])
ARQUIVO_DADO_6 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado6.png'])
ARQUIVO_DADO_0 = sep.join([path.dirname(path.abspath(__file__)), '..', 'assets', 'dado0.png'])

screen = None  # tela a ser configurada
imagem_fundo = None  # imagem de fundo que vai ser carregada
rect_imagem_fundo = None  # objeto da image de fundo que vai ser carregada
dict_peoes = {}  # dicionario para guardar os peoes (cache)
dict_posicoes = None  # dicionario para posicoes (gerado no inicializar)

font_texto = None

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

lista_chat = None   # cada elemento eh [frase, cor]

imagens_peca = {}
dict_peoes_multiplos = {}

imagens_dado = {}
valor_dado_anterior = 6


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
    global font_texto
    global som_peca, som_captura, som_vitoria, som_dado
    global botao_musica_on, rect_botao_musica, botao_musica_off
    global botao_som_on, botao_som_off, rect_botao_som
    global lista_chat
    global imagens_peca, imagens_dado

    print("Iniciando pygame: ", end='')

    pygame.init()
    screen = pygame.display.set_mode(TAMANHO_TELA)
    pygame.display.set_caption("Ludo")

    # MUSICA
    print("Musica, ", end='')
    pygame.mixer.music.load(ARQUIVO_MUSICA)
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(loops=True, fade_ms=1000)

    # SOM
    print("Som, ", end='')
    som_peca = pygame.mixer.Sound(ARQUIVO_SOM_PECA)
    som_captura = pygame.mixer.Sound(ARQUIVO_SOM_CAPTURA)
    som_vitoria = pygame.mixer.Sound(ARQUIVO_SOM_VITORIA)
    som_dado = pygame.mixer.Sound(ARQUIVO_SOM_DADO)

    # BOTOES
    print("Botoes, ", end='')
    botao_musica_on = pygame.image.load(ARQUIVO_BOTAO_MUSICA_ON)
    rect_botao_musica = botao_musica_on.get_rect()
    rect_botao_musica.x, rect_botao_musica.y = POS_BOTAO
    botao_musica_off = pygame.image.load(ARQUIVO_BOTAO_MUSICA_OFF)

    botao_som_on = pygame.image.load(ARQUIVO_BOTAO_SOM_ON)
    rect_botao_som = botao_som_on.get_rect()
    rect_botao_som.x, rect_botao_som.y = POS_BOTAO[0], POS_BOTAO[1] + 50 + 20
    botao_som_off = pygame.image.load(ARQUIVO_BOTAO_SOM_OFF)

    # FUNDO
    print("Fundo, ", end='')
    imagem_fundo = pygame.image.load(ARQUIVO_FUNDO)
    rect_imagem_fundo = imagem_fundo.get_rect()
    rect_imagem_fundo.x = 0
    # (COMPRIMENTO_TELA - ALTURA_TELA) // 2  # posiciona no centro
    rect_imagem_fundo.y = 0

    # POSICOES
    print("Posicoes, ", end='')
    with open(ARQUIVO_POSICOES, 'r') as f:
        # o arquivo esta como 'str': [int, int]. Mas eu quero int: [int, int]
        # por isso, vou converter para inteiro todas as chaves
        # lambda vai ser uma funcao que recebe o dic, e retorna faz um dict comprehension
        # que pega a chave, transforma em int, e atribui ao conteudo, pego atraves de dict.items()
        dict_posicoes = load(f, object_hook=lambda d: {int(a): b for a, b in d.items()})
    # print("DONE")

    # print("Carrengando peoes: ", end="")
    _monta_cache_peoes(c)
    # print("DONE")

    # TEXTOS
    print("Textos, ", end='')
    font_texto = pygame.font.SysFont('bahnschrift.ttf', 34, bold=False)
    lista_chat = list()
    lista_chat.append(("Bem vindo ao Ludo!", 'default'))

    # pecas
    print("Pecas, ", end='')
    imagens_peca['red'] = pygame.image.load(ARQUIVO_PECA_VERMELHO)
    imagens_peca['green'] = pygame.image.load(ARQUIVO_PECA_VERDE)
    imagens_peca['blue'] = pygame.image.load(ARQUIVO_PECA_AZUL)
    imagens_peca['yellow'] = pygame.image.load(ARQUIVO_PECA_AMARELO)
    imagens_peca['selecao'] = pygame.image.load(ARQUIVO_PECA_SELECAO)

    # DADOS
    print("Dados, ", end='')
    imagens_dado[1] = pygame.image.load(ARQUIVO_DADO_1)
    imagens_dado[2] = pygame.image.load(ARQUIVO_DADO_2)
    imagens_dado[3] = pygame.image.load(ARQUIVO_DADO_3)
    imagens_dado[4] = pygame.image.load(ARQUIVO_DADO_4)
    imagens_dado[5] = pygame.image.load(ARQUIVO_DADO_5)
    imagens_dado[6] = pygame.image.load(ARQUIVO_DADO_6)
    imagens_dado[0] = pygame.image.load(ARQUIVO_DADO_0)

    print("\nFINALIZADO.")
    return


def _checa_eventos():
    """
    Verifica a interacao com a interface grafica.
    Se o jogo fechar, ele fecha sem salvar.
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


def _desenha_dado(valor):
    imagem = imagens_dado[valor]
    rect_dado = imagem.get_rect()
    rect_dado.x, rect_dado.y = 152, 593
    screen.blit(imagem, rect_dado)
    return


def _desenha_destaque(pos):
    x, y = dict_posicoes[pos]
    x += 280
    imagem_peca = imagens_peca['selecao']
    rect_peao = imagem_peca.get_rect()
    rect_peao.x, rect_peao.y = x - 1, y - 1
    screen.blit(imagem_peca, rect_peao)
    return


def _desenha_peao(cor, pos):
    """
    Tenta desenhar um peao na tela.
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

    # SOBREPOSICAO DE PEOES
    if pos in dict_peoes_multiplos:
        lista = dict_peoes_multiplos[pos]

        quantidade_pecas = lista[0]
        posicao_dentro = quantidade_pecas - len(lista) + 1  # 0 até (quantidade - 1)
        cor = lista.pop(1)  # tira uma cor qualquer da lista.

        # distribuir igualmente de (5,5) ate (28, 23)
        pos_x = 23 // (quantidade_pecas - 1) * posicao_dentro + 5 + x
        pos_y = 17 // (quantidade_pecas - 1) * posicao_dentro + 5 + y

        imagem_peca = pygame.transform.scale(imagens_peca[cor], (15, 20))
        rect_peao = imagem_peca.get_rect()
        rect_peao.x, rect_peao.y = pos_x, pos_y

        screen.blit(imagem_peca, rect_peao)
    # FIM DA SOBREPOSICAO DE PEOES

    else:
        imagem_peca = imagens_peca[cor]
        rect_peao = imagem_peca.get_rect()
        rect_peao.x, rect_peao.y = x + 10, y + 4
        screen.blit(imagem_peca, rect_peao)


def _monta_peoes_multiplos():
    """Monta o dicionario com as posicoes, e os peoes que tem la (so se tiver mais de 1)"""
    global dict_peoes_multiplos

    dict_peoes_multiplos.clear()
    dict_temp = {}
    for p in dict_peoes:
        cor = dict_peoes[p][0]
        pos = dict_peoes[p][1]
        if pos not in dict_temp:
            dict_temp[pos] = [cor]
        else:
            dict_temp[pos].append(cor)

    for d in dict_temp:
        if len(dict_temp[d]) > 1:
            dict_peoes_multiplos[d] = [len(dict_temp[d])] + dict_temp[d]   # [q, cor1, cor2, cor3...]

    return


def _atualiza_peao(c, i):
    """Recebe um id, e atualiza o cache interno."""
    p = baseDados.selecionar_tabuleiro(c, peao=i)
    dict_peoes[i][1] = p['pos']


def atualiza_tela(c=None, atualizar=None, destacar=None, travar_destaque=False, chat=None, dado=None):
    """
    Atualiza a tela da interface do jogo.
    Se atualizar for uma lista de ids:
        Esses peoes serao atualizados
        Precis da conexao com a base de dados
    Se destacar for uma lista de ids:
        Esses peoes serao destacados.
    Se travar_destaque, os destaques nao seram excluidos
    """
    global lista_chat, valor_dado_anterior

    # screen.fill(COR_PRETO)  # fundo preto
    screen.blit(imagem_fundo, rect_imagem_fundo)  # imagem de fundo
    if bool_tocar_musica:
        screen.blit(botao_musica_on, rect_botao_musica)
    else:
        screen.blit(botao_musica_off, rect_botao_musica)

    if bool_tocar_som:
        screen.blit(botao_som_on, rect_botao_som)
    else:
        screen.blit(botao_som_off, rect_botao_som)

    if dado is not None:
        valor_dado_anterior = dado
    _desenha_dado(valor_dado_anterior)

    if atualizar is not None:  # atualiza os peoes no cache
        for p in atualizar:
            _atualiza_peao(c, p)

    if destacar is not None:  # prepara os peoes a serem destacados
        for p in destacar:
            dict_peoes[p][2] = True

    _monta_peoes_multiplos()  # cria o dicionario como peoes multiplos, pra o desenho usar

    for p in dict_peoes:  # PRIMEIRA PASSAGEM (DESENHA OS DESTAQUES):
        peao = dict_peoes[p]
        if peao[2]:
            _desenha_destaque(peao[1])

    for p in dict_peoes:  # SEGUNDA PASSAGEM (DESENHA OS PEOES):
        peao = dict_peoes[p]
        _desenha_peao(peao[0], peao[1])

        if destacar is not None:
            if p not in destacar:
                dict_peoes[p][2] = False
        elif not travar_destaque:
            dict_peoes[p][2] = False

    if chat is not None:
        lista_chat.insert(0, chat)
        if len(lista_chat) == 15:
            lista_chat.pop()

    for i, (frase, cor) in enumerate(lista_chat):
        texto = font_texto.render(frase, True, CORES[cor])
        rect_texto = texto.get_rect()
        rect_texto.x, rect_texto.y = (COMPRIMENTO_TELA + ALTURA_TELA) // 2 + 10, ALTURA_TELA - 30 - 30 * i
        screen.blit(texto, rect_texto)

    pygame.display.flip()  # atualiza a tela


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
                if x1 <= x <= x1 + 48 and y1 <= y <= y1 + 48:
                    return i


def roda_dado():
    """Espera ele clicar no dado"""
    while True:
        pos = _checa_eventos()
        if pos is not None:  # o mouse foi clicado
            x, y = pos
            if 152 <= x <= 252 and 593 <= y <= 693:
                return


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


def espera_tempo(ms):
    """Congela o jogo."""
    pygame.time.wait(ms)  # espera ms


def exibe_tela_final_e_fecha(vencedores):
    """Exibe tela de vitoria e fecha o jogo depois de 10 segundos."""
    atualiza_tela(chat=("Jogo encerrado!", 'default'))
    atualiza_tela(chat=("Ranking", 'default'))
    for i, vencedor in enumerate(vencedores):
        atualiza_tela(chat=("%d°: %s" % (i + 1, vencedor), vencedor))  # imprime os vencedores

    atualiza_tela(chat=('', 'default'))
    atualiza_tela(chat=("Fechando em 10s", 'default'))
    t = time()
    while time() - t <= 10:  # loop de 10 segundos
        _checa_eventos()

    fechar()
