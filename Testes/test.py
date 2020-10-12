import unittest
from Jogador.jogador import *
from Peca.peca import *
from Casa.casa import *


class Testes_jogador(unittest.TestCase):

    def test_criar_jogador(self):
        jogador = cria_jogador(1, 'marcos')
        self.assertEqual(get_id_jogador(jogador), 1)
        self.assertEqual(get_nome_jogador(jogador), 'marcos')


class Testes_peca(unittest.TestCase):
    def test_cria_peca(self):
        peca = cria_peca(1, 'amarelo')
        self.assertEqual(get_peca_cor(peca), 'amarelo')
        self.assertEqual(get_peca_uid(peca), 1)


class Testes_casa(unittest.TestCase):
    def test_cria_casa(self):
        casa = cria_casa(1, 'amarelo', True)
        self.assertEqual(get_casa_cor(casa), 'amarelo')
        self.assertEqual(get_casa_uid(casa), 1)
        self.assertEqual(get_casa_is_especial(casa), True)


if __name__ == '__main__':
    unittest.main()
