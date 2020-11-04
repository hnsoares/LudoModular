import mysql.connector
from mysql.connector import Error

_BD = "ludomodular"
_TABELA_PECAS = 'pecas'
_TABELA_TABULEIRO = 'tabuleiro'


def _pegar_credenciais():
    """
    Pega credenciais do BD em credenciais.txt
    O arquivo é estruturado da seguinte maneira:
    'host'
    'user'
    password'
    """
    try:
        with open('credenciais.txt', 'r') as f:
            return f.read().split('\n')
    except Exception as e:
        print("Nao consegui pegar credenciais do BD: " % e)
        return None


def _conectar_mysql_jogo():
    """
    Conecta com a base de dados do jogo a ser usado.
    Retorna 0 se sucesso.
    Retorna Error se nao conseguiu
    """
    credenciais = _pegar_credenciais()
    if credenciais is None:
        return None
    try:
        c = mysql.connector.connect(
            host=credenciais[0],
            user=credenciais[1],
            password=credenciais[2],
            database=_BD
        )
        return c
    except Error as e:
        return e


def _conectar_mysql():
    """
    Pega as credenciais e conecta com o BD.
    Retorna o objeto do conector se sucesso,
    retorna Error se falhou.
    """

    credenciais = _pegar_credenciais()

    if credenciais is None:
        return None
    try:
        c = mysql.connector.connect(
            host=credenciais[0],
            user=credenciais[1],
            password=credenciais[2]
        )
        return c
    except Error as e:
        return e


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


def inicar_conexao():
    c = _conectar_mysql_jogo()  # conecta diretamente ao BD do jogo
    if c is Error:  # pode nao existir o BD jogo
        c = _conectar_mysql()
        if c is Error:  # nao conseguiu nem conectar sem ser no jogo
            print("Erro de conexao: ", c)
            return None

        _criar_bd_jogo(c)  # cria o BD do jogo
        c.close()
        c = _conectar_mysql_jogo()  # tenta novamente a conexao

    if c is Error:  # o erro nao era o BD do jogo...
        print("Erro de conexao ao MySQL ", c)
        return None

    print("Conectado ao MySQL " + c.get_server_info())

    cursor = c.cursor()

    # excluindo todas as tabelas antigas
    for t in [_TABELA_PECAS, _TABELA_TABULEIRO]:
        q = "DROP TABLE IF EXISTS %s" % t
        cursor.execute(q)
    c.commit()

    # criando a tabela para os peoes
    q = "CREATE TABLE %s (id INTEGER, cor VARCHAR(30), primary key (id))" % _TABELA_PECAS
    cursor.execute(q)
    print("Tabela de peoes criada")

    # criando a tabela para o tabuleiro
    q = """
    CREATE TABLE %s (
    id INTEGER, 
    pos INTEGER, 
    pos_inicial INTEGER,
    eh_finalizado INTEGER,
    eh_inicio INTEGER,
    primary key (id))
    """ % _TABELA_TABULEIRO

    cursor.execute(q)
    print("Tabela de tabuleiro criada")

    c.commit()
    cursor.close()
    return c


def fechar_conexao(c):
    """Encerra a conexao com o MySQL."""

    if c.is_connected():
        cursor = c.cursor()
        cursor.execute("DROP TABLE IF EXISTS pecas ")
        cursor.execute("DROP TABLE IF EXISTS tabuleiro")
        c.commit()
        cursor.close()
        c.close()

    print("Conexao encerrada.")
    return


def adicionar_peao(c, id_peca, cor_peca):
    """
    Adiciona o peao e sua cor na tabela.
    Retorna None.
    """
    cursor = c.cursor()
    q = "INSERT INTO %s " % _TABELA_PECAS + " (id, cor) VALUES (%s, %s)"
    val = (id_peca, cor_peca)
    cursor.execute(q, val)
    c.commit()
    cursor.close()
    return


def selecionar_peca(c, peca):
    """
    Procura a cor daquele peca.
    Retorna a cor se achar, ou '' se nao achar.
    """
    cursor = c.cursor()
    q = "SELECT cor FROM %s WHERE id=%d" % (_TABELA_PECAS, peca)
    cursor.execute(q)
    r = cursor.fetchone()

    cursor.close()
    if r is None:
        return ''
    return r[0]


def limpar_peao(c):
    """Limpa a tabela com as pecas."""
    cursor = c.cursor()
    q = "DELETE FROM %s" % _TABELA_PECAS
    cursor.execute(q)
    c.commit()
    cursor.close()
    return


# def adicionar_tabuleiro(c, peao, pos, pos_inicial, eh_inicio, eh_finalizado):
#     pass


# def selecionar_tabuleiro(c, peao=None, pos=None):
#     pass


# def limpar_tabuleiro(c):
#    pass


if __name__ == '__main__':
    pass