'''
Módulo feito por Marcos Vinicius
inicio: 10/10/2020
fim: 17/10/2020
'''


import json

__all__ = ['salva_partida', 'carrega_partida']


def salva_partida(partida):
    '''
    -->Recebe um dicionário partida
    <--Retorna 1 se o processo foi concluido
    '''
    arq = open('partida.json', "w", encoding='utf-8')
    json.dump(partida, arq)
    arq.close()
    return 1


def carrega_partida(arquivo):
    '''
    --> Recebe um arquivo .json que representa a partida
    <-- Retorna a partida
    '''
    json_file = open(arquivo, "r", encoding="utf-8")
    partida = json.load(json_file)
    json_file.close()
    return partida
