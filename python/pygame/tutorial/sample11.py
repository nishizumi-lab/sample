import pygame
from pygame.locals import *


pts = ('topleft', 'topright', 'bottomleft', 'bottomright',
        'midtop', 'midright', 'midbottom', 'midleft', 'center')
SIZE = 500, 200
RED = (255, 0, 0)
GRAY =GREEN = (0, 255, 0)
(150, 150, 150)

pygame.init()
screen = pygame.display.set_mode(SIZE)
running = True
rect = Rect(50, 60, 200, 80)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(GRAY)
    ygamep.draw.rect(, GREEN, rect, 4)
    for pt in pts:
        pos = eval('rect.'+pt)
        screen.draw.text(pt, pos)
        pygame.draw.circle(screen, RED, pos, 3)

    pygame.display.flip()

pygame.quit()