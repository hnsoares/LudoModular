"""
Main da build #1
"""


import pygame
#partida.rodar_partida()
pygame.init()

X_SCREEN = 800
Y_SCREEN = 600
screen = pygame.display.set_mode((X_SCREEN,Y_SCREEN))#tamanho
pygame.display.set_caption("LUDO") #titulo

x = 10
y = 500
width = 40
height = 60
vel = 10
running = True


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

button = Button('blue', 100, 100, 100, 40, 'Teste')
while running:
    pygame.time.delay(50)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
    button.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pos = pygame.mouse.get_pos()
        if button.isOver(pos):
            print('Clicou no botão')
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and x <= X_SCREEN - width:
        x += vel
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel



pygame.quit()
