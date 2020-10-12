__all__ = ["cria_casa", "get_casa_uid", "get_casa_cor", "get_casa_is_especial"]


def cria_casa(uid, cor, is_special):
    return {
        "uid": uid,
        "color": cor,
        "is_special": is_special
    }


def get_casa_uid(casa):
    return casa['uid']


def get_casa_cor(casa):
    return casa['cor']


def get_casa_is_especial(casa):
    return casa['is_especial']
