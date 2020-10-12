__all__ = ["cria_peca", "get_peca_cor", "get_peca_uid"]


def cria_peca(uid, cor):
    return {
        "uid": uid,
        "color": cor
    }


def get_peca_cor(peca):
    return peca['cor']


def get_peca_uid(peca):
    return peca['uid']
