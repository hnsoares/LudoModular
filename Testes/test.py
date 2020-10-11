import unittest
from Jogador.jogador import *


class Testes_jogador(unittest.TestCase):

    def test_criar_jogador(self):
        jogador = cria_jogador(1, 'marcos')
        self.assertEqual(get_id_jogador(jogador), 1)
        self.assertEqual(get_nome_jogador(jogador), 'marcos')


if __name__ == '__main__':
    unittest.main()
