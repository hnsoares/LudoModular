'''
Módulo feito por João Santana
início: 16/09/2020
fim: 20/09/2020
'''


__all__ = ["cria_peca", "get_peca_cor", "get_peca_uid"]


def cria_peca(uid, cor):  # uid e cor sao int
    '''
    --> Recebe uid e cor
    <-- Retorna um dic
    '''
    if cor not in range(4):
        return 0
    return {
        "uid": uid,
        "color": cor
    }


def get_peca_cor(peca):
    return peca['cor']


def get_peca_uid(peca):
    return peca['uid']
