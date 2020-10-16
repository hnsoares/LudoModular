import unittest
from unittest.mock import Mock
from Jogo.jogador import cria_jogador
from Jogo.tabuleiro import cria_tabuleiro, altera_tabuleiro


class TestJogador(unittest.TestCase):
    def test_cria_jogador(self):
        jog = cria_jogador(1, 'marcos')
        self.assertEqual(jog['nome'], 'marcos')
        jog = cria_jogador(1, 'marc!s')
        self.assertEqual(jog, 0)

class TestTabuleiro(unittest.TestCase):
    def test_cria_tabuleiro(self):
        tabuleiro = cria_tabuleiro(4)
        self.assertEqual(len(tabuleiro), 92) #testando se o tabuleiro tem o tamanho certo
        tabuleiro = cria_tabuleiro(10) #criando tabuleiro com mais de 4 jogadores
        self.assertEqual(tabuleiro, 0)

    def test_altera_tabuleiro(self):
        tabuleiro = cria_tabuleiro(4)
        self.assertEqual(altera_tabuleiro(tabuleiro, 1, 10), 0, 'Acessando uma peça existente...')
        #self.assertEqual(altera_tabuleiro(tabuleiro, 40, 10), 1)


if __name__ == '__main__':
    unittest.main()
