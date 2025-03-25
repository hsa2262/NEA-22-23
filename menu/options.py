import pygame
import sys
from settings.settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("NEA project")
font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 34)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def options():
    options_button = pygame.Rect(270, 50, 220, 55)
    pygame.draw.rect(screen, (0, 0, 0), options_button)
    draw_text("OPTIONS", font, (255, 255, 255), screen, options_button.left + 17, options_button.center[1] - 15)

    return options_button


runs = True
while runs:
    options_button = options()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    screen.fill("black")
    clock.tick(FPS)
