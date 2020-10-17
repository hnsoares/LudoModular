from Jogo.partida import cria_partida
from Jogo.saveload import salva_partida, carrega_partida
partida = cria_partida({})
salva_partida(partida)
partida2 = carrega_partida('partida.txt')
print(partida == partida2)
print('Partida criada com sucesso!')

