from Jogo.partida import cria_partida
from Jogo.saveload import salva_partida, carrega_partida
partida = cria_partida({})
if partida != {}:
    print('Partida criada com sucesso!')

