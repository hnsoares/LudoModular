"""
Módulo para armazenamento permanente de Dados.
A sua função é guardar os arquivos da base de dados e armazenar em arquivos XML.

Funcoes:
    detecta_partida_completa()
    recupera_partida_completa(c)
    salva_partida_completa(c, [dados])

Feita por Daniel
"""

from dados import baseDados
import xml.etree.ElementTree as ET
from xml.dom import minidom
from os import path, sep, remove  # so para o armazenamento funcionar e para remover uma partida salva

PATH = path.dirname(path.abspath(__file__)) + sep + 'arquivos' + sep
ARQUIVO_PARTIDA = 'partida.xml'


def _converte_objeto(o, tipo):
    """Recebe o tipo de objeto e converte."""
    if tipo == 'str':
        return str(o)
    if tipo == 'int':
        return int(o)
    if tipo == 'float':
        return float(o)

    print('erro de conversao!', o, tipo)
    return None


def _coletar_peoes(c):
    """Pega uma lista com todas as peoes."""
    cursor = c.cursor(dictionary=True)
    q = "SELECT * FROM %s" % baseDados.TABELA_PEOES
    cursor.execute(q)
    r = cursor.fetchall()
    cursor.close()
    return r


def _coletar_tabuleiro(c):
    """Pega uma lista com todas as peoes no tabuleiro."""
    cursor = c.cursor(dictionary=True)
    q = "SELECT * FROM %s" % baseDados.TABELA_TABULEIRO
    cursor.execute(q)
    r = cursor.fetchall()
    cursor.close()
    return r


def _formata_xml(xml):
    # copia dos slides 15
    s1 = ET.tostring(xml, 'utf-8')
    s2 = minidom.parseString(s1)
    return s2.toprettyxml(indent="    ")


def salvar_partida_completa(c, dados=None):
    """
    Salva os dados da partida em um arquivo para ser recuperado depois.
    Os dados seguem as seguintes restricoes:
        Devem ser um dicionario com as chaves todas como string
        Ele aceita valores de conteudo como int, float ou string
        Ele aceita que o valor seja uma lista, porem:
            Todos os elementos devem ser do mesmo tipo.
            Os elementos seguem as mesmas regras acima (int, float, string)
    Retorna 0
    """

    peoes = _coletar_peoes(c)  # coleta as peoes do BD
    tabuleiro = _coletar_tabuleiro(c)  # coleta as peoes no tabuleiro do BD

    jogo = ET.Element('jogo')  # topo do xml
    jogo.append(ET.Comment("Dados de uma partida de ludo"))

    # para peoes e tabuleiros, preciso criar um elemento
    # depois, criar um elemento para cada objeto, e com seus dados,
    # criar um elemento para cada dado, setando o seu tipo e seu conteudo

    elementos_peoes = ET.SubElement(jogo, 'peoes')  # guardando as peoes
    for p in peoes:
        elemento_peao = ET.SubElement(elementos_peoes, 'peao')
        for d in p:
            elemento_dado = ET.SubElement(elemento_peao, d)  # chave do dicionario
            elemento_dado.text = str(p[d])  # conteudo do dicionario
            elemento_dado.set('tipo', str(type(p[d]).__name__))  # armazena o tipo da variavel para converter dps

    # repete a mesma coisa para o tabuleiro
    elementos_tabuleiro = ET.SubElement(jogo, 'tabuleiros')
    for t in tabuleiro:
        elemento_tabuleiro = ET.SubElement(elementos_tabuleiro, 'tabuleiro')
        for d in t:
            elemento_dado = ET.SubElement(elemento_tabuleiro, d)
            elemento_dado.text = str(t[d])
            elemento_dado.set('tipo', str(type(t[d]).__name__))

    # para dados, eh mais complicado.
    # funciona parecido, mas eh mais geral
    # se o dado for uma lista, preciso converter toda a lista.
    #   CONSIDERANDO QUE TODOS OS ELEMENTOS DA LISTA SAO DO MESMO TIPO

    if dados is not None:
        elemento_dados = ET.SubElement(jogo, 'dados')
        for d in dados:
            if type(dados[d]) == list:  # se o dado for uma lista
                elemento_dado = ET.SubElement(elemento_dados, d)
                elemento_dado.text = ','.join([str(x) for x in dados[d]])  # junta tudo com virgulas
                elemento_dado.set('tipo', 'list')
                if not dados[d]:
                    elemento_dado.set('subtipo', 'str')   # se a lista estiver vazia, fala que eh string
                else:
                    elemento_dado.set('subtipo', str(type(dados[d][0]).__name__))  # pega o tipo do primeiro

            elif type(dados[d]) not in [str, int, float]:
                print("Nao consegui armazenar o dado:", d, dados[d])
            else:
                elemento_dado = ET.SubElement(elemento_dados, d)
                elemento_dado.text = str(dados[d])
                elemento_dado.set('tipo', str(type(dados[d]).__name__))

    saida = _formata_xml(jogo)  # copia dos slides 15
    with open(PATH + ARQUIVO_PARTIDA, "w+") as f:
        f.write(saida)

    return 0


def detecta_partida_completa():
    """
    Detecta se ha uma partida salva.
    Retorna True/False
    """
    nome_arquivo = PATH + ARQUIVO_PARTIDA
    return path.exists(nome_arquivo)


def recupera_partida_completa(c):
    """
    Recupera a partida salva e joga no BD.
    Recupera também os dados extras e retorna o dicionario como fornecido para salvar
    Retorna None se nao tiver nenhuma partida salva.
    """

    nome_arquivo = PATH + ARQUIVO_PARTIDA
    try:
        with open(nome_arquivo, 'r') as f:
            tree = ET.parse(f)
            jogo = tree.getroot()

    except FileNotFoundError:
        return None

    lista_peoes = []
    lista_tabuleiro = []

    # LENDO AS peoes
    peoes = jogo.find('peoes')
    for peao in peoes.findall('peao'):
        d = dict()
        for atr in peao:
            # print(atr.tag, atr.attrib['tipo'], atr.text)
            # tag = nome do atributo
            # text = conteudo do atributo
            # attrib['tipo'] = tipo do atributo para converter
            d[atr.tag] = _converte_objeto(atr.text, atr.attrib['tipo'])
        lista_peoes.append(d)

    # ESCREVENDO NA BASE DE DADOS
    baseDados.limpar_peao(c)
    for peao in lista_peoes:
        baseDados.adicionar_peao(c, peao['id'], peao['cor'])

    # LENDO OS TABULEIROS
    baseDados.limpar_tabuleiro(c)
    tabuleiros = jogo.find('tabuleiros')
    for tabuleiro in tabuleiros.findall('tabuleiro'):
        d = dict()
        for atr in tabuleiro:
            # print(atr.tag, atr.attrib['tipo'], atr.text)
            # tag = nome do atributo
            # text = conteudo do atributo
            # attrib['tipo'] = tipo do atributo para converter
            d[atr.tag] = _converte_objeto(atr.text, atr.attrib['tipo'])
        lista_tabuleiro.append(d)

    # ESCREVENDO NA BASE DE DADOS
    for tab in lista_tabuleiro:
        # pode ser otimizada a usar executemany do SQL
        baseDados.adicionar_tabuleiro(c, tab['id'], tab['pos'], tab['pos_inicial'],
                                      tab['eh_inicio'], tab['eh_finalizado'])

    # RECUPERANDO OS DADOS
    dados = jogo.find('dados')
    if dados is None:
        return {}

    # todos os dados sao filhos de "dados"

    dicionario_dados = dict()
    for dado in dados:
        # print(dado.tag, dado.attrib['tipo'], dado.text)
        if dado.attrib['tipo'] == 'list':
            if dado.text is None:
                dicionario_dados[dado.tag] = []
            else:
                dicionario_dados[dado.tag] = [_converte_objeto(x, dado.attrib['subtipo']) for x in dado.text.split(",")]
        else:
            dicionario_dados[dado.tag] = _converte_objeto(dado.text, dado.attrib['tipo'])

    return dicionario_dados


def exclui_partida_completa():
    nome_arquivo = PATH + ARQUIVO_PARTIDA
    if detecta_partida_completa():
        remove(nome_arquivo)
    return
