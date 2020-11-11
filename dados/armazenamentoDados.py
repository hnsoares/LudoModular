"""
Módulo para armazenamento permanente de Dados.
A sua função é guardar os arquivos da base de dados e armazenar em arquivos XML.
"""

from dados import baseDados
# import mysql.connector
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
    dados eh um dicionario com informacoes genericas. Deve ser chave -> int/float/string
    Retorna 0
    """

    peoes = _coletar_peoes(c)  # coleta as peoes do BD
    tabuleiro = _coletar_tabuleiro(c)  # coleta as peoes no tabuleiro do BD

    jogo = ET.Element('jogo')  # topo do xml
    jogo.append(ET.Comment("Dados de uma partida de ludo"))

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

    # dados quaisquer. o dicionario precisa ser chave <string> -> <int, float, string> para conseguir converter
    if dados is not None:
        elemento_dados = ET.SubElement(jogo, 'dados')
        for d in dados:
            if type(dados[d]) == list:
                elemento_dado = ET.SubElement(elemento_dados, d)
                elemento_dado.text = ','.join([str(x) for x in dados[d]])
                elemento_dado.set('tipo', 'list')
                if not dados[d]:
                    elemento_dado.set('subtipo', 'str')
                else:
                    elemento_dado.set('subtipo', str(type(dados[d][0]).__name__))

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


def exclui_partida_completa():
    """
    Exclui uma partida que havia sido salva.
    0 se sucesso,
    -1 se nao havia partida
    """
    nome_arquivo = PATH + ARQUIVO_PARTIDA
    if path.exists(nome_arquivo):
        remove(nome_arquivo)
        return 0
    return -1


def recupera_partida_completa(c):
    """
    Recupera a partida salva e joga no BD. Recupera também os dados extras e retorna o dicionario.
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
            dicionario_dados[dado.tag] = [_converte_objeto(x, dado.attrib['subtipo']) for x in dado.text.split(",")]
        else:
            dicionario_dados[dado.tag] = _converte_objeto(dado.text, dado.attrib['tipo'])

    return dicionario_dados


if __name__ == "__main__":
    conexao = baseDados.iniciar_conexao()
    try:
        baseDados.adicionar_peao(conexao, 0, 'vermelho')
        baseDados.adicionar_peao(conexao, 1, 'rosa')

        baseDados.adicionar_tabuleiro(conexao, 1, 2, 3, True, False)
        baseDados.adicionar_tabuleiro(conexao, 4, 5, 6, False, True)

        algum_dado = {'tempo': 100, 'turno': 'vermelho'}

        salvar_partida_completa(conexao, dados=algum_dado)

        # print(coletar_peoes(x))
    except Exception as e:
        print(e)
    finally:
        baseDados.fechar_conexao(conexao)
