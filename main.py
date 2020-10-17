from Jogo.partida import cria_partida
from Jogo.saveload import salva_partida, carrega_partida
from Jogo.tabuleiro import cria_tabuleiro, altera_tabuleiro
partida = cria_partida({})
if partida != {}:
    print('Partida criada com sucesso!')

tabuleiro = cria_tabuleiro(4)
a = altera_tabuleiro(tabuleiro, 0, 4)

print(a)
print(tabuleiro[:5])
