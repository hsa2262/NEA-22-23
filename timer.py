import pygame
import sys
from settings.settings import *


pygame.init()
screen = pygame.display.set_mode((GWIDTH, GHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("NEA project")
font = pygame.font.Font("fonts/FreePixel.ttf", 34)

sec = 0
mins = 0
hours = 0
text = font.render("{}:{}:{}".format(hours, mins, sec), True, (255, 255, 255), (0, 0, 0))
textRect = text.get_rect()
textRect.center = (GWIDTH // 2, 50)


while True:

    clock.tick(1)
    sec += 1
    screen.blit(text, textRect)
    if sec == 60:
        sec = 0
        mins += 1
    if mins == 60:
        mins = 0
        sec = 0
        hours += 1

    text = font.render("{}:{}:{}".format(hours, mins, sec), True, (255, 255, 255), (0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #screen.fill("white")

    pygame.display.update()
    clock.tick(FPS)
