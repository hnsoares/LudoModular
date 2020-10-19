'''
Módulo feito por Marcos Vinicius
inicio: 18/09/2020
fim: 22/09/2020
'''


__all__ = ["cria_casa", "get_casa_uid", "get_casa_cor", "get_casa_is_especial"]


def cria_casa(uid, cor, is_special):  # uid e cor sao int
    '''
    -->Recebe como parâmetro uid, cor e uma variavel booleana
    <--Retorna um dic com os respectivos parametros
    '''
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


def testa_casa(dic, key):
    try:
        dic[key]
    except KeyError:
        return 0
    return 1
