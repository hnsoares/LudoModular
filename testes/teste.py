import unittest
from unittest.mock import Mock
import jogo.peao
import jogo.tabuleiro
import jogo.dado
import jogo.partida
import dados.baseDados as BD
import dados.armazenamentoDados as AD

conexao_bd = BD.iniciar_conexao()  # para ser usado durante os testes da BaseDados
if not conexao_bd.is_connected():
    raise Exception('naoConectou')


class TestesBaseDados(unittest.TestCase):
    def test_limpando_tabuleiro(self):
        BD.adicionar_tabuleiro(conexao_bd, 99, 0, 0, False, False)
        x = BD.limpar_tabuleiro(conexao_bd)
        self.assertEqual(0, x, 'limpando tabuleiro')
        x = BD.selecionar_tabuleiro(conexao_bd, 99)
        self.assertEqual(-1, x, 'limpando tabuleiro 2')

    def test_limpando_peao(self):
        BD.adicionar_peao(conexao_bd, 99, 'vermelho')
        x = BD.limpar_peao(conexao_bd)
        self.assertEqual(0, x, 'limpando peao')
        x = BD.selecionar_peao(conexao_bd, 99)
        self.assertEqual('', x, 'limpando peao 2')

    def test_adicionar_peao(self):
        BD.limpar_peao(conexao_bd)
        x = BD.adicionar_peao(conexao_bd, 0, 'vermelho')
        self.assertEqual(0, x, 'adicionando peao bd')
        x = BD.adicionar_peao(conexao_bd, 0, 'rosa')
        self.assertEqual(-1, x, 'adicionando conexao bd 2')

    def test_selecionar_peao(self):
        BD.limpar_peao(conexao_bd)
        BD.adicionar_peao(conexao_bd, 1, 'rosa')
        x = BD.selecionar_peao(conexao_bd, 1)
        self.assertEqual('rosa', x, 'achando peao')

    def test_adicionar_tabuleiro(self):
        BD.limpar_tabuleiro(conexao_bd)
        x = BD.adicionar_tabuleiro(conexao_bd, 0, 1, 2, True, False)
        self.assertEqual(0, x, 'adicionando tabuleiro')
        x = BD.adicionar_tabuleiro(conexao_bd, 0, 101, 202, False, True)
        self.assertEqual(-1, x, 'adicionando tabuleiro 2')

    def test_selecionar_tabuleiro(self):
        BD.limpar_tabuleiro(conexao_bd)
        BD.adicionar_tabuleiro(conexao_bd, 1, 2, 3, False, True)
        x = BD.selecionar_tabuleiro(conexao_bd, peao=1)
        r = {'id': 1, 'pos': 2, 'pos_inicial': 3, 'eh_inicio': False, 'eh_finalizado': True}
        self.assertDictEqual(r, x, 'selecionando tabuleiro')
        x = BD.selecionar_tabuleiro(conexao_bd, pos=2)
        self.assertDictEqual(x[0], r, 'selecionando tabuleiro 2')

    def test_modificar_tabuleiro(self):
        BD.limpar_tabuleiro(conexao_bd)
        BD.adicionar_tabuleiro(conexao_bd, 2, 0, 0, True, False)
        x = BD.modificar_tabuleiro(conexao_bd, 2, 10, 20, False, False)
        self.assertEqual(x, 0, 'modificando tabuleiro')
        x = BD.selecionar_tabuleiro(conexao_bd, peao=2)
        r = {'id': 2, 'pos': 10, 'pos_inicial': 20, 'eh_inicio': False, 'eh_finalizado': False}
        self.assertDictEqual(r, x, 'modificando tabuleiro 2')


class TestesArmazenamentoDados(unittest.TestCase):

    def test_salvar_partida_completa(self):
        BD.limpar_tabuleiro(conexao_bd)
        BD.limpar_peao(conexao_bd)
        BD.adicionar_peao(conexao_bd, 0, 'azul')
        BD.adicionar_tabuleiro(conexao_bd, 0, 1, 2, True, False)
        dados = {'bom': 'dia'}
        x = AD.salvar_partida_completa(conexao_bd, dados)
        self.assertEqual(x, 0, 'salvando partida')

    def test_exclui_partida_completa(self):
        AD.salvar_partida_completa(conexao_bd)
        x = AD.exclui_partida_completa()
        self.assertEqual(0, x, 'excluindo partida 1')
        x = AD.exclui_partida_completa()
        self.assertEqual(-1, x, 'excluindo partida 2')

    def test_recupera_partida_completa(self):
        dados = {'boa': 'tarde'}
        AD.salvar_partida_completa(conexao_bd, dados)
        x = AD.recupera_partida_completa(conexao_bd)
        self.assertDictEqual(x, dados, 'recuperando partida 1')
        AD.exclui_partida_completa()
        x = AD.recupera_partida_completa(conexao_bd)
        self.assertIsNone(x, 'recuperando partida 2')


class TestesPeao(unittest.TestCase):

    def test_criacao_peao(self):
        jogo.peao.limpar_peoes(conexao_bd)
        x = jogo.peao.criar_peao(conexao_bd, 'amarelo')
        self.assertEqual(jogo.peao.acessar_peao(conexao_bd, x), 'amarelo', "Acessando peão criado.")
        self.assertEqual(jogo.peao.acessar_peao(conexao_bd, 19999), '', "Acessando peão inexistente.")

    def test_limpando_peao(self):
        x = jogo.peao.criar_peao(conexao_bd, 'roxo')
        self.assertEqual(jogo.peao.acessar_peao(conexao_bd, x), 'roxo', "Acessando peão antes delete")
        jogo.peao.limpar_peoes(conexao_bd)
        self.assertEqual(jogo.peao.acessar_peao(conexao_bd, x), '', 'Acessando peao apos limpar.')

    def test_criando_varios_peoes(self):
        # cada id tem que ser diferente
        d = dict()
        for i in range(30):
            x = jogo.peao.criar_peao(conexao_bd, 'branco')
            self.assertTrue(x not in d, 'tentando criar muitos peoes')
            d[x] = 1


class TestesTabuleiro(unittest.TestCase):

    def test_iniciar_tabuleiro(self):
        self.assertEqual(jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4), 0, 'Iniciando tabuleiro com 4 pessoas.')
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [1, 2, 3, 4])
        self.assertEqual(jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 5), 0, 'Iniciando tabuleiro com 5 pessoas.')
        self.assertEqual(jogo.tabuleiro.reiniciar_peao(conexao_bd, 1), -1, 'tentando usar peao que nao existe mais.')

    def test_adicionar_peoes(self):
        # 0 -> sucesso
        # 1 -> id_repetido
        # 2 -> lista invalida
        # 3 -> limite maximo atingido
        jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4)
        lista1 = [0, 1, 2, 3]
        lista2 = [5, 6, 7, 8]
        lista3 = [9, 10, 11]
        lista4 = [100, 200, 300, 400]
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, lista1)
        self.assertEqual(x, 0, 'Adicionado peoes simples.')
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, lista1)
        self.assertEqual(x, 1, 'adicionando novamente os peoes.')
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, lista2)
        self.assertEqual(x, 0, 'adicionando outros peoes')
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, lista3, lista1)
        self.assertEqual(x, 2, 'adicionando com posicao invalida')
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, [90, 100, 110, 120], lista4)
        self.assertEqual(x, 0, 'adicionando com posicao certa')
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [34, 35, 36, 37])
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, [111, 222, 333, 444])
        self.assertEqual(x, 3, 'adicionando com limite maximo atingido')
        jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4)
        x = jogo.tabuleiro.adicionar_peoes(conexao_bd, [])
        self.assertEqual(x, 2, 'adicionando uma lista vazia')

    def test_acessar_posicao(self):
        jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4)
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [1, 2, 3, 4], [5, 6, 7, 7])
        self.assertIn(1, jogo.tabuleiro.acessar_posicao(conexao_bd, 5), 'acessando posicao')
        self.assertIn(2, jogo.tabuleiro.acessar_posicao(conexao_bd, 6), 'acessando posicao')
        self.assertIn(3, jogo.tabuleiro.acessar_posicao(conexao_bd, 7), 'acessando posicao')
        self.assertIn(4, jogo.tabuleiro.acessar_posicao(conexao_bd, 7), 'acessando posicao')
        self.assertEqual(jogo.tabuleiro.acessar_posicao(conexao_bd, 0), 0)

    def test_reiniciar_peao(self):
        jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4)
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [1, 2, 3, 4], [1, 2, 3, 4])
        self.assertEqual(0, jogo.tabuleiro.reiniciar_peao(conexao_bd, 1), 'reiniciando peao')
        self.assertEqual(-1, jogo.tabuleiro.reiniciar_peao(conexao_bd, 6), 'reiniciando peao nao existente')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 1, 4), 1, 'tentando mover peao reiniciado')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 2, 3), 0, 'mover peao nao reiniciado')

    def test_movimentacao_possivel(self):
        jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4)
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [1, 2, 3, 4])
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [5, 6, 7, 8], [1005, 1004, 0, 0])
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 1, 3), 1, 'tentando mover inicio')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 2, 3), 1, 'tentando mover inicio')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 5, 3), 2, 'tentando mover finalizado')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 7, 6), 0, 'tentando mover inicio com 6')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 6, 1), 0, 'tentando mover pra casa final')
        self.assertEqual(jogo.tabuleiro.movimentacao_possivel(conexao_bd, 123, 123), -1, 'mover peao inexistente')

    def test_mover_peao(self):
        jogo.tabuleiro.iniciar_tabuleiro(conexao_bd, 4)
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [1, 2, 3, 4])
        jogo.tabuleiro.adicionar_peoes(conexao_bd, [5, 6, 7, 8], [13, 10, 2000, 2004])
        self.assertEqual(jogo.tabuleiro.mover_peao(conexao_bd, 1, 6), 0, 'movendo peao pra casa 0')
        self.assertEqual(jogo.tabuleiro.mover_peao(conexao_bd, 2, 6), 0, 'tirando outro peao do inicio')
        self.assertEqual(jogo.tabuleiro.mover_peao(conexao_bd, 5, 3), 13 + 3, 'movendo um peao normalmente')
        self.assertTrue(jogo.tabuleiro.mover_peao(conexao_bd, 6, 6) > 2000, 'movendo pra reta final')
        self.assertEqual(jogo.tabuleiro.mover_peao(conexao_bd, 7, 3), 2003, 'movendo dentro da casa final')
        self.assertEqual(jogo.tabuleiro.mover_peao(conexao_bd, 8, 1), -2, 'finalizando um peao')
        self.assertEqual(jogo.tabuleiro.mover_peao(conexao_bd, 123, 123), -1, 'movendo um inexistente')


class TestesDado(unittest.TestCase):
    def test_rodar_dado(self):
        x = jogo.dado.jogar_dado()
        self.assertTrue(1 <= x <= 6)


class TestesPartida(unittest.TestCase):
    def test_criar_partida(self):
        x = jogo.partida._criar_partida(False)
        self.assertEqual(x, 0, 'criando partida')

    def test_rodada(self):
        jogo.partida._criar_partida()
        jogo.partida.escolher_peao = Mock(return_value=0)  # overwrite a escolha do peao
        cores = jogo.partida.LISTA_CORES
        for i in range(20):  # fazer 20 rodadas, ver se todas deram certo.
            x = jogo.partida._rodada(cores[i % 4])
            self.assertTrue(0 <= x <= 3, 'fazendo uma _rodada')

    # def test_rodar_partida(self):
    #     jogo.partida._criar_partida()
    #     jogo.partida.escolher_peao = Mock(return_value=0)  # overwrite a escolha do peao
    #     x = jogo.partida._rodar_partida()
    #     self.assertEqual(x, 0, 'rodando a partida')

    # escolher_peao eh uma funcao temporaria (enquanto nao ha graficos)
    # cor_da_rodada eh um gerador, nao uma funcao. Por isso nao ha testes





if __name__ == '__main__':
    unittest.main()
