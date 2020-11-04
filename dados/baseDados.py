import mysql.connector


def pegar_credenciais():
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


def conectar_mysql():
    """
    Pega as credenciais e conecta com o BD.
    Retorna o objeto do conector se sucesso,
    retorna None se falhou.
    """

    credenciais = pegar_credenciais()
    if credenciais is None:
        return None

    conexao = mysql.connector.connect(
        host=credenciais[0],
        user=credenciais[1],
        password=credenciais[2]
    )

    return conexao


def criar_bd(c):
    """
    Cria o BD a ser usado se ja nao existir.
    Recebe o connect do mysql
    Retorna 1 se sucesso
    Retorna 0 se ja existia
    """

    bd = "ludomodular"

    cursor = c.cursor()
    cursor.execute("SHOW DATABASES")
    r = cursor.fetchall()

    for b in r:  # ('nome_bd',)
        if bd in b:  # verifica se bd esta no nome acima
            return 0  # pula fora

    q = "CREATE DATABASE " + bd
    cursor.execute(q)
    cursor.close()
    return 1


def fechar_conexao(c):
    """Recebe a conexao e a encerra."""
    if c.is_connected():
        c.close()

    print("Conexao encerrada.")
    return


conexao = conectar_mysql()
print(criar_bd(conexao))
fechar_conexao(conexao)
