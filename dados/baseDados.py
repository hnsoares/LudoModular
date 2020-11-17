"""
Módulo para base de dados.
Sua função é gerir a base, e servir para acessar e modificar dados.

Caso a conexão não funcione, confira se o arquivo credenciais.txt está configurada corretamente.
Mais informações no arquivo README.MD

Funções:
    iniciar_conexao()
    fechar_conexao(c)

    limpar_peao(c)
    limpar_tabuleiro(c)

    adicionar_peao(c, cor)
    adicionar_tabuleiro(c, id, pos, pos_inicial, eh_inicio, eh_finalizado)

    selecionar_peao(c, [peao], [cor])
    selecionar_tabuleiro(c, [peao], [pos])

    modificar_tabuleiro(c, id, pos, pos_inicial, eh inicio, eh finalizado)

Feita por Daniel
"""


import mysql.connector
from mysql.connector import Error
from os import path, sep  # so para as credenciais funcionarem


_BD = "ludomodular"  # nome do banco de dados
TABELA_PEOES = 'peoes'
TABELA_TABULEIRO = 'tabuleiro'


def _pegar_credenciais():
    """
    Pega credenciais do BD em credenciais.txt
    O arquivo é estruturado da seguinte maneira:
    'host'
    'user'
    password'
    """
    p = path.dirname(path.abspath(__file__)) + sep + 'arquivos' + sep  # cria o path para o arquivo

    try:
        with open(p + 'credenciais.txt', 'r') as f:
            return f.read().split('\n')
    except Exception as e:
        print("Nao foi possivel achar o arquivo credenciais.txt. Leia o README.md para mais informacoes.")
        print("Erro lendo arquivo: ", e)
        exit(0)
        # return None


def _conectar_mysql_jogo():
    """
    Conecta com a base de dados do jogo a ser usado.
    Retorna o conector se sucesso.
    Retorna Error se nao conseguiu
    """
    credenciais = _pegar_credenciais()
    if credenciais is None:
        return None
    c = mysql.connector.connect(
        host=credenciais[0],
        user=credenciais[1],
        password=credenciais[2],
        database=_BD  # mesma coisa que a funcao abaixo, mas com o BD
    )
    return c


def _conectar_mysql():
    """
    Pega as credenciais e conecta com o BD.
    Retorna o objeto do conector se sucesso,
    Retorna Error se falhou.
    """

    credenciais = _pegar_credenciais()

    if credenciais is None:
        return None
    c = mysql.connector.connect(
        host=credenciais[0],
        user=credenciais[1],
        password=credenciais[2]
    )
    return c


def _criar_bd_jogo(c):
    """
    Cria o BD a ser usado se ja nao existir.
    Recebe o connect do mysql geral.
    Retorna 1 se sucesso.
    Retorna 0 se ja existia.
    """

    cursor = c.cursor()
    cursor.execute("SHOW DATABASES")
    r = cursor.fetchall()

    for b in r:  # ('nome_bd',)
        if _BD in b:  # verifica se bd esta no nome acima
            return 0  # pula fora

    q = "CREATE DATABASE " + _BD
    cursor.execute(q)
    cursor.close()
    return 1


def _iniciar_tabelas(c):
    """Cria as tabelas no Banco de Dados."""

    cursor = c.cursor()

    # excluindo todas as tabelas antigas
    # for t in [TABELA_PEOES, TABELA_TABULEIRO]:
    #     q = "DROP TABLE IF EXISTS %s" % t
    #     cursor.execute(q)
    # c.commit()

    # criando a tabela para os peoes
    q = "CREATE TABLE IF NOT EXISTS %s (id INTEGER, cor VARCHAR(30), primary key (id))" % TABELA_PEOES
    cursor.execute(q)
    # print("Tabela de peoes criada")

    # criando a tabela para o tabuleiro
    q = """
    CREATE TABLE IF NOT EXISTS %s (
    id INTEGER, 
    pos INTEGER, 
    pos_inicial INTEGER,
    eh_inicio INTEGER,
    eh_finalizado INTEGER,
    primary key (id))
    """ % TABELA_TABULEIRO

    cursor.execute(q)
    # print("Tabela de tabuleiro criada")

    c.commit()
    cursor.close()
    return


def iniciar_conexao():
    """
    Estabelece uma conexao com o banco de dados.
    Retorna o objeto, ou levanta erro..
    """
    try:
        c = _conectar_mysql_jogo()  # tento conectar com a base de dados
    except Error:  # se nao existir
        try:
            c = _conectar_mysql()  # conecto sem ser na base de dados
            _criar_bd_jogo(c)  # crio ela
            c.close()  # fecho a conexao
            c = _conectar_mysql_jogo()  # recomeco outra conexao, dessa vez com a base de dados
        except Error as e:  # se ainda nao conseguir
            print("Nao consegui criar uma base de dados: ", e)
            print("Abortando.")
            exit(1)

    # se consegui conectar com a base de dados
    print("Conectado ao MySQL " + c.get_server_info())

    _iniciar_tabelas(c)
    print("Tabelas montadas.")
    # limpar_peao(c)
    # limpar_tabuleiro(c)

    return c


def fechar_conexao(c):
    """
    Encerra a conexao com o MySQL.
    Nao retorna nada.
    """

    if c.is_connected():
        cursor = c.cursor()
        cursor.execute("DROP TABLE IF EXISTS pecas ")
        cursor.execute("DROP TABLE IF EXISTS tabuleiro")
        c.commit()
        cursor.close()
        c.close()

    print("Conexao encerrada.")
    return


def adicionar_peao(c, id_peao, cor_peao):
    """
    Adiciona o peao e sua cor na tabela.
    Retorna 0 ou -1 se ja havia.
    """

    cursor = c.cursor()
    q = "INSERT INTO %s " % TABELA_PEOES + " (id, cor) VALUES (%s, %s)"
    val = (id_peao, cor_peao)
    try:
        cursor.execute(q, val)
        c.commit()
    except mysql.connector.IntegrityError:  # ja havia um peao com aquele id
        return -1
    cursor.close()
    return 0


def selecionar_peao(c, peao=None, cor=None):
    """
    Retorna informacao dos peoes no tabuleiro.
    Se peao for um id:
        Retorna cor do peao se achar o id.
        Retorna '' se nao tiver peao com aquele id
    Se nao, se uma cor for definida:
        Retorna uma lista com os ids dos peoes daquela cor
    """

    cursor = c.cursor()
    if peao is not None:
        q = "SELECT cor FROM %s WHERE id=%d" % (TABELA_PEOES, peao)
        cursor.execute(q)
        r = cursor.fetchone()
        cursor.close()
        if r is None:
            return ''
        return r[0]  # (cor,) -> precisa levar so a cor

    if cor is not None:
        q = "SELECT id FROM %s WHERE cor='%s'" % (TABELA_PEOES, cor)
        cursor.execute(q)
        r = cursor.fetchall()
        cursor.close()
        if r is None:
            return None
        r = [x[0] for x in r]  # pega o primeiro valor da tupla (id) de cada resposta
        return r


def limpar_peao(c):
    """
    Limpa a tabela com os peoes.
    Retorna 0
    """
    cursor = c.cursor()
    q = "DELETE FROM %s" % TABELA_PEOES
    # q = "TRUNCATE TABLE %s" % TABELA_PEOES
    cursor.execute(q)
    c.commit()
    cursor.close()
    return 0


def adicionar_tabuleiro(c, peao, pos, pos_inicial, eh_inicio, eh_finalizado):
    """
    Adiciona o peao e suas informacoes na tabela do tabuleiro.
    Retorna 0 no sucesso.
    Retorna -1 se ja havia um peao com aquele id.
    """
    cursor = c.cursor()
    q = "INSERT INTO %s " % TABELA_TABULEIRO +\
        "(id, pos, pos_inicial, eh_inicio, eh_finalizado) VALUES (%s, %s, %s, %s, %s)"

    val = (peao, pos, pos_inicial, 1 if eh_inicio else 0, 1 if eh_finalizado else 0)
    try:
        cursor.execute(q, val)
        c.commit()
    except mysql.connector.IntegrityError:  # ja havia um peao com aquele id
        return -1
    cursor.close()
    return 0


def _converter_tupla_dic(tupla):
    """
    Converte a tupla de um elemento do tabuleiro em um dicionario.
    Pode ser substituido por c.cursor(dictionary=True).
    """
    # (id, pos, pos_inicial, eh_inicio, eh_finalizado)
    d = dict()
    d['id'] = tupla[0]
    d['pos'] = tupla[1]
    d['pos_inicial'] = tupla[2]
    d['eh_inicio'] = True if tupla[3] == 1 else False  # converte int para bool
    d['eh_finalizado'] = True if tupla[4] == 1 else False  # converte int para bool

    return d


def selecionar_tabuleiro(c, peao=None, pos=None):
    """
    Retorna um dicionario com os dados do peao no tabuleiro
    Retorna -1 se nao existir aquele peao/pos.
    """
    # cursor = c.cursor(dictionary=True)
    cursor = c.cursor()
    if peao is not None:
        q = "SELECT * FROM %s WHERE id=%d" % (TABELA_TABULEIRO, peao)
        cursor.execute(q)
        r = cursor.fetchone()
        cursor.close()

        if r is None:
            return -1
        return _converter_tupla_dic(r)

    if pos is not None:
        # vendo pela posicao
        q = "SELECT * FROM %s WHERE pos=%d" % (TABELA_TABULEIRO, pos)
        cursor.execute(q)
        r = cursor.fetchall()
        cursor.close()
        for i in range(len(r)):
            r[i] = _converter_tupla_dic(r[i])
        return r


def modificar_tabuleiro(c, peao, pos, pos_inicial, eh_finalizado, eh_inicio):
    """
    Atualiza a peca com essas informacoes
    Retorna 0
    """
    cursor = c.cursor()
    # a estrategia eh remover e adicionar.
    # pode ser trocado pelo UPDATE futuramente

    # remove peca do tabuleiro
    q = "DELETE FROM %s WHERE id=%d" % (TABELA_TABULEIRO, peao)
    cursor.execute(q)

    # adiciona ela novamente
    adicionar_tabuleiro(c, peao, pos, pos_inicial, eh_finalizado, eh_inicio)

    cursor.close()
    return 0


def limpar_tabuleiro(c):
    """
    Limpa a tabela com as pecas no tabuleiro.
    Retorna 0
    """
    cursor = c.cursor()
    q = "DELETE FROM %s" % TABELA_TABULEIRO
    # q = "TRUNCATE TABLE %s" % TABELA_TABULEIRO
    cursor.execute(q)
    c.commit()
    cursor.close()
    return 0
