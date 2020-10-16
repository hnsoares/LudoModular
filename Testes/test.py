import unittest
from Jogador.jogador import *
from Peca.peca import *
from Casa.casa import *
from Tabuleiro.tabuleiro import *


class Testes_jogador(unittest.TestCase):
    def test_criar_jogador(self):
        jogador = cria_jogador(1, 'pedro')
        self.assertEqual(get_nome_jogador(jogador), 'pedro',
                         'Acessando jogador existente...')
        self.assertEqual(get_nome_jogador(10000), '',
                         'Acessando jogador inexistente...')


class Testes_peca(unittest.TestCase):
    def test_cria_peca(self):
        peca = cria_peca(1, 1)
        self.assertEqual(get_peca_cor(peca), 1, 'Acessando cor existente')
        self.assertEqual(get_peca_uid(1999), 0, 'Acessando peao inexistente')


class Testes_casa(unittest.TestCase):
    def test_cria_casa(self):
        casa = cria_casa(1, 'amarelo', True)
        self.assertEqual(get_casa_cor(casa), 'amarelo')
        self.assertEqual(get_casa_uid(casa), 1)
        self.assertEqual(get_casa_is_especial(casa), True)


class Testes_tabuleiro(unittest.TestCase):
    def test_cria_tabuleiro(self):
        tabuleiro = []
        retorno = cria_tabuleiro(4, tabuleiro)
        self.assertEqual(retorno, 1, 'Tabuleiro criado sem problemas.')
        retorno = cria_tabuleiro(10, tabuleiro)
        self.assertEqual(retorno, 0, 'Numero de jogadores excedido...')


if __name__ == '__main__':
    unittest.main()
