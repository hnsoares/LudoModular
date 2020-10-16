import json

__all__ = ['salvar_partida']


def salvar_partida(partida):
    '''
    with open('./partida.json') as f:
        lista_jogadores_json = json.dumps(partida['lista_jogadores'])
    '''
    arq = open('save.csv', 'w')
    string = ''
    for jogador in partida['lista_jogadores']:
        string += str(jogador) + ','

    string = string[:-1] + '\n'

    arq.write(string)
