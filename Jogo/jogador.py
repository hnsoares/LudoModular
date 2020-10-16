'''
Módulo feito por Marcos Vinicius
início: 22/09/2020
fim: 25/09/2020
'''

__all__ = ["cria_jogador"]


def cria_jogador(uid, nome):  # uid é um int e nome é uma string
    '''
    --> Recebe uid e nome
    <-- Retorna dic com os respectivos campos
    <-- Retorna 0 caso possua um caracter especial
    '''
    for el in '#$%¨&*!@':
        if el in nome:
            return 0
    return {
        "id": uid,
        "nome": nome
    }


def set_id_jogador(jogador, uid):
    jogador["id"] = uid
    return jogador


def set_nome_jogador(jogador, nome):
    jogador["nome"] = nome
    return jogador


def get_nome_jogador(jogador):
    return jogador["nome"]


def get_id_jogador(jogador):
    return jogador["id"]
