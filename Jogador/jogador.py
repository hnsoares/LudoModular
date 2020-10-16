__all__ = ["cria_jogador", "set_id_jogador",
           "set_nome_jogador", "get_nome_jogador", "get_id_jogador"]


def cria_jogador(uid, nome):  # uid é um int e nome é uma string
    '''
    --> Recebe uid e nome
    <-- Retorna dic com os respectivos campos
    '''
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
