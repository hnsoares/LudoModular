'''
Testes feitos por Marcos Vinicius
início: 25/09/2020
fim: 09/10/2020
'''

import unittest
from unittest.mock import Mock
from Jogo.jogador import cria_jogador
from Jogo.tabuleiro import cria_tabuleiro, altera_tabuleiro
from Jogo.casa import cria_casa
from Jogo.peca import cria_peca
from Jogo.partida import cria_partida


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
        self.assertEqual(altera_tabuleiro(tabuleiro, 1, 4), 1, 'Acessando uma peça existente...')
        self.assertEqual(altera_tabuleiro(tabuleiro, 20, 4), 1, 'Acessando um peça inexistente')

class TestCasa(unittest.TestCase):
    def test_cria_casa(self):
        '''
        1 -> verde
        2 -> vermelho
        3 -> amarelo
        4 -> azul
        '''
        casa = cria_casa(1, 1, True)
        self.assertEqual(casa['color'], 1, 'Acessando cor da casa...')
        self.assertEqual(casa['uid'], 1, 'Acessando uid da casa...')
        self.assertEqual(casa['is_special'], 1, 'Checando se a casa é especial...')

class TestPeca(unittest.TestCase):
    def test_cria_peca(self):
        '''
        1 -> verde
        2 -> vermelho
        3 -> amarelo
        4 -> azul
        '''
        peca = cria_peca(1, 1)
        self.assertEqual(peca['color'], 1, 'Acessando cor da peca...')
        self.assertEqual(peca['uid'], 1, 'Acessando uid da peça...')

class TestPartida(unittest.TestCase):
    def test_cria_partida(self):
        jogadores = ['marcos', 'joao', 'henrique', 'flavio']
        print('Para testar a função cria_partida, coloque 1 para o número de jogadores e "a" para o nome.')
        partida = cria_partida({})
        partida['lista_jogadores'] = jogadores
        self.assertEqual(partida['turno'], 0)
        self.assertEqual(partida['lista_jogadores'],  jogadores)

if __name__ == '__main__':
    unittest.main()
