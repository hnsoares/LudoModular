import unittest
from unittest.mock import Mock
import jogo.peao
import jogo.tabuleiro
import jogo.dado
import jogo.partida


class TestesPeao(unittest.TestCase):
    def test_criacao_peao(self):
        jogo.peao.limpar_peoes()
        x = jogo.peao.criar_peao('amarelo')
        self.assertEqual(jogo.peao.acessar_peao(x), 'amarelo', "Acessando peão criado.")
        self.assertEqual(jogo.peao.acessar_peao(19999), '', "Acessando peão inexistente.")

    def test_limpando_peao(self):
        x = jogo.peao.criar_peao('roxo')
        self.assertEqual(jogo.peao.acessar_peao(x), 'roxo', "Acessando peão antes delete")
        jogo.peao.limpar_peoes()
        self.assertEqual(jogo.peao.acessar_peao(x), '', 'Acessando peao apos limpar.')

    def test_criando_varios_peoes(self):
        # cada id tem que ser diferente
        d = dict()
        for i in range(30):
            x = jogo.peao.criar_peao('branco')
            self.assertTrue(x not in d, 'tentando criar muitos peoes')
            d[x] = 1


class TestesTabuleiro(unittest.TestCase):
    def test_iniciar_tabuleiro(self):
        self.assertEqual(jogo.tabuleiro.iniciar_tabuleiro(4), 0, 'Iniciando tabuleiro com 4 pessoas.')
        jogo.tabuleiro.adicionar_peoes([1, 2, 3, 4])
        self.assertEqual(jogo.tabuleiro.iniciar_tabuleiro(5), 0, 'Iniciando tabuleiro com 5 pessoas.')
        self.assertEqual(jogo.tabuleiro.reiniciar_peao(1), -1, 'tentando usar peao que nao existe mais.')

    def test_adicionar_peoes(self):
        # 0 -> sucesso
        # 1 -> id_repetido
        # 2 -> lista invalida
        # 3 -> limite maximo atingido
        jogo.tabuleiro.iniciar_tabuleiro(4)
        lista1 = [0, 1, 2, 3]
        lista2 = [5, 6, 7, 8]
        lista3 = [9, 10, 11]
        lista4 = [100, 200, 300, 400]
        x = jogo.tabuleiro.adicionar_peoes(lista1)
        self.assertEqual(x, 0, 'Adicionado peoes simples.')
        x = jogo.tabuleiro.adicionar_peoes(lista1)
        self.assertEqual(x, 1, 'adicionando novamente os peoes.')
        x = jogo.tabuleiro.adicionar_peoes(lista2)
        self.assertEqual(x, 0, 'adicionando outros peoes')
        x = jogo.tabuleiro.adicionar_peoes(lista3, lista1)
        self.assertEqual(x, 2, 'adicionando com posicao invalida')
        x = jogo.tabuleiro.adicionar_peoes([90, 100, 110, 120], lista4)
        self.assertEqual(x, 0, 'adicionando com posicao certa')
        jogo.tabuleiro.adicionar_peoes([34, 35, 36, 37])
        x = jogo.tabuleiro.adicionar_peoes([111, 222, 333, 444])
        self.assertEqual(x, 3, 'adicionando com limite maximo atingido')
        jogo.tabuleiro.iniciar_tabuleiro(4)
        x = jogo.tabuleiro.adicionar_peoes([])
        self.assertEqual(x, 2, 'adicionando uma lista vazia')

    def test_acessar_posicao(self):
        jogo.tabuleiro.iniciar_tabuleiro(4)
        jogo.tabuleiro.adicionar_peoes([1, 2, 3, 4], [5, 6, 7, 7])
        self.assertIn(1, jogo.tabuleiro.acessar_posicao(5), 'acessando posicao')
        self.assertIn(2, jogo.tabuleiro.acessar_posicao(6), 'acessando posicao')
        self.assertIn(3, jogo.tabuleiro.acessar_posicao(7), 'acessando posicao')
        self.assertIn(4, jogo.tabuleiro.acessar_posicao(7), 'acessando posicao')
        self.assertEqual(jogo.tabuleiro.acessar_posicao(0), 0)

    def test_reiniciar_peao(self):
        jogo.tabuleiro.iniciar_tabuleiro(4)
        jogo.tabuleiro.adicionar_peoes([1, 2, 3, 4], [1, 2, 3, 4])
        self.assertEqual(0, jogo.tabuleiro.reiniciar_peao(1), 'reiniciando peao')
        self.assertEqual(-1, jogo.tabuleiro.reiniciar_peao(6), 'reiniciando peao nao existente')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(1, 4), 1, 'tentando mover peao reiniciado')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(2, 3), 0, 'tentando mover peao nao reiniciado')

    def test_movimentacao_possivel(self):
        jogo.tabuleiro.iniciar_tabuleiro(4)
        jogo.tabuleiro.adicionar_peoes([1, 2, 3, 4])
        jogo.tabuleiro.adicionar_peoes([5, 6, 7, 8], [1005, 1004, 0, 0])
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(1, 3), 1, 'tentando mover inicio')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(2, 3), 1, 'tentando mover inicio')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(5, 3), 2, 'tentando mover finalizado')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(7, 6), 0, 'tentando mover inicio com 6')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(6, 1), 0, 'tentando mover pra casa final')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(123, 123), -1, 'tentando mover peao inexistente')

    def test_mover_peao(self):
        jogo.tabuleiro.iniciar_tabuleiro(4)
        jogo.tabuleiro.adicionar_peoes([1, 2, 3, 4])
        jogo.tabuleiro.adicionar_peoes([5, 6, 7, 8], [13, 10, 2000, 2004])
        self.assertEqual(jogo.tabuleiro.mover_peao(1, 6), 0, 'movendo peao pra casa 0')
        self.assertEqual(jogo.tabuleiro.mover_peao(2, 6), 0, 'tirando outro peao do inicio')
        self.assertEqual(jogo.tabuleiro.mover_peao(5, 3), 13+3, 'movendo um peao normalmente')
        self.assertTrue(jogo.tabuleiro.mover_peao(6, 6) > 2000, 'movendo pra reta final')
        self.assertEqual(jogo.tabuleiro.mover_peao(7, 3), 2003, 'movendo dentro da casa final')
        self.assertEqual(jogo.tabuleiro.mover_peao(8, 1), -2, 'finalizando um peao')
        self.assertEqual(jogo.tabuleiro.mover_peao(123, 123), -1, 'movendo um inexistente')


class TestesDado(unittest.TestCase):
    def test_rodar_dado(self):
        x = jogo.dado.jogar_dado()
        self.assertTrue(1 <= x <= 6)


class TestesPartida(unittest.TestCase):
    def test_criar_partida(self):
        x = jogo.partida.criar_partida()
        self.assertEqual(x, 0, 'criando partida')

    def test_rodada(self):
        jogo.partida.criar_partida()
        jogo.partida.escolher_peao = Mock(return_value=0)  # overwrite a escolha do peao
        cores = jogo.partida.LISTA_CORES
        for i in range(20):  # fazer 20 rodadas, ver se todas deram certo.
            x = jogo.partida.rodada(cores[i % 4])
            self.assertTrue(0 <= x <= 3, 'fazendo uma rodada')

    def test_rodar_partida(self):
        jogo.partida.criar_partida()
        jogo.partida.escolher_peao = Mock(return_value=0)  # overwrite a escolha do peao
        x = jogo.partida.rodar_partida()
        self.assertEqual(x, 0, 'rodando a partida')

    # escolher_peao eh uma funcao temporaria (enquanto nao ha graficos)
    # cor_da_rodada eh um gerador, nao uma funcao. Por isso nao ha testes


if __name__ == '__main__':
    unittest.main()
