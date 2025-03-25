import pygame, sys
from settings.settings import *


pygame.init()
screen = pygame.display.set_mode((GWIDTH, GHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("NEA project")
font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 34)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def question():
    question = pygame.Rect(230, 50, 500, 55)
    pygame.draw.rect(screen, (0, 0, 0), question)
    draw_text("Would you like to use up your", font, (255, 255, 255), screen, question.left + 22, question.center[1] - 17)
    return question


def question2():
    question2 = pygame.Rect(250, 100, 500, 55)
    pygame.draw.rect(screen, (0, 0, 0), question2)
    draw_text("items to summon the witch?", font, (255, 255, 255), screen, question2.left + 22, question2.center[1] - 17)
    return question2


def yes():
    yes_button = pygame.Rect(370, 200, 100, 55)
    pygame.draw.rect(screen, (0, 0, 0), yes_button)
    draw_text("yes", font, (255, 255, 255), screen, yes_button.left + 22, yes_button.center[1] - 17)
    return yes_button


def no():
    no_button = pygame.Rect(520, 200, 100, 55)
    pygame.draw.rect(screen, (0, 0, 0), no_button)
    draw_text("no", font, (255, 255, 255), screen, no_button.left + 32, no_button.center[1] - 17)
    return no_button


while True:
    yes_button = yes()
    no_button = no()
    question_button = question()
    question_button2 = question2()

    click = False
    x, y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    if yes_button.collidepoint((x, y)):
        pygame.draw.rect(screen, (0, 0, 0), yes_button)
        draw_text("yes", font, (0, 150, 100), screen, yes_button.left + 22, yes_button.center[1] - 17)
        if click:
            import enemy_encounters.witch_encounter
    if no_button.collidepoint((x, y)):
        pygame.draw.rect(screen, (0, 0, 0), no_button)
        draw_text("no", font, (140, 0, 50), screen, no_button.left + 32, no_button.center[1] - 17)
        if click:
            quit()

    pygame.display.update()
    screen.fill("black")
    clock.tick(FPS)
