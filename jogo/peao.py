# -*- coding: utf-8 -*-
"""
Módulo Peao

limpar_peoes()
criar_peao()
acessar_peao()

28/09 (Guilherme): Modulo criado
05/10 (Daniel): Recomecando (deletando classes)
05/10 (Daniel): Movimentacao do Peao
05/10 (Daniel): Refazendo peao (peao so contem cor)
06/10 (Daniel): Atualizando acessar_peao
"""

peoes = []
id_peao_atual = 0


def limpar_peoes():
    """Limpa todos os peoes salvos. Retorna 0."""
    global id_peao_atual
    peoes.clear()
    id_peao_atual = 0
    return 0


def criar_peao(cor):
    """Cria um peao. Retorna seu id."""
    global id_peao_atual
    peao = dict()

    peao['id'] = id_peao_atual
    id_peao_atual += 1
    peao['cor'] = cor
    peoes.append(peao)
    return peao['id']


def acessar_peao(id_peao):
    """Acessa a cor do peao. Retorna:
    cor
    string vazia se nao existir esse id.
    """
    for p in peoes:
        if p['id'] == id_peao:
            return p['cor']
    return ''
