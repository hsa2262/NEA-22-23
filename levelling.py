import pygame
import sys
from settings.settings import *


pygame.init()
screen = pygame.display.set_mode((GWIDTH, GHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("NEA project")
font = pygame.font.Font("Fonts/FreePixel.ttf", 34)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


level = 1
exp = (level/0.5)**2
exp_received = 4

if exp_received >= exp:
    level += 1

while True:

    draw_text(f"Level: {level}", font, (255, 255, 255), 10, 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #screen.fill("grey")

    pygame.display.update()
    clock.tick(FPS)
