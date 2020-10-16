import unittest
from unittest.mock import Mock
import Jogo.jogador


class Test_jogador(unittest.TestCase):
    def test_cria_jogador(self):
        jog = Jogo.jogador.cria_jogador(1, 'marcos')
        self.assertEqual(Jogo.jogador.get_nome_jogador(jog), 'marcos')
        jog = Jogo.jogador.cria_jogador(1, 'marc!s')
        self.assertEqual(Jogo.jogador.get_nome_jogador(jog), 0)


if __name__ == '__main__':
    unittest.main()
