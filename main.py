"""
Main da build #1
"""
import pygame
from display.menu import Button


#iniciar modulos de terceiros
pygame.init()

#constantes para tela
X_SCREEN = 800
Y_SCREEN = 600

#constantes para o botão
HEIGHT_BUTTON = 50
WIDTH_BUTTON = 150

#pygame
tela = pygame.display.set_mode((X_SCREEN, Y_SCREEN))#tamanho
pygame.display.set_caption("LUDO")
iniciar = Button('red', 300, 300, WIDTH_BUTTON, HEIGHT_BUTTON, 'Iniciar')
config = Button('blue', 300, 370, WIDTH_BUTTON, HEIGHT_BUTTON, 'Configurações')
fechar = Button('purple', 300, 440, WIDTH_BUTTON, HEIGHT_BUTTON, 'Fechar')

running = True
while running:
    tela.fill((255, 255, 255))

    iniciar.draw(tela)
    config.draw(tela)
    fechar.draw(tela)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('Jogo finalizado')
        #preciso clicar primeiro
        pos = pygame.mouse.get_pos()
        if iniciar.isOver(pos):
            print('Iniciando o jogo...')
        if config.isOver(pos):
            print('Abrindo as configurações...')
        if fechar.isOver(pos) and pygame.mouse.get_pressed():
            running = False
            print('Jogo finalizado')


pygame.quit()
