__all__ = ["cria_jogador", "set_id_jogador", "set_nome_jogador"]


def cria_jogador(uid, nome):
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
