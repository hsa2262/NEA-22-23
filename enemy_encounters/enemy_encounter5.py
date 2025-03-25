import pygame
import sys
from settings.settings import *
import os
import os.path
from tiles.level2 import Level
from tiles.game_data import level_0
from inventory import UserInterface

# dialogue when interacting with final boss
with open(r"/Users/ashleylim/PycharmProjects/NEA project/dialogue_text.txt", 'r') as fp:
    # lines to read
    line_numbers = [46, 47, 48]
    # To store lines
    final_dialogue = []
    for i, line in enumerate(fp):
        if i in line_numbers:
            final_dialogue.append(line.strip())

# screen
pygame.init()
screen = pygame.display.set_mode((GWIDTH, GHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("NEA project")
font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 34)
level = Level(level_0, screen)
icon = pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/images/icon.png").convert_alpha()
icon = pygame.transform.scale(icon, (30 * 5, 22 * 5))
new_font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 26)

# variables
left = False
right = False
scroll = 0
bg_scroll = 0
RIGHT_THRESH = 200  # how far the player can get to the edge of the screen
LEFT_THRESH = 70  # how far the player can get to the edge of the screen

items = pygame.sprite.Group()

# background
bg_images = []
for i in range(1, 4):
    bg_image = pygame.image.load(f"/Users/ashleylim/PycharmProjects/NEA project/background/background_layer_{i}.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (320 * 1.35, 180 * 1.35))
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


def draw_bg():
    for x in range(5):
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll, 0))


# instructions screen
def instructions():
    pygame.init()

    def draw_text(text, font, text_col, x, y):
        img = new_font.render(text, True, text_col)
        screen.blit(img, (x, y))

    run = True
    while run:

        draw_text("- MOVE LEFT: 'A' KEY or LEFT", font, (255, 255, 255), 10, 20)
        draw_text("ARROW KEY", font, (255, 255, 255), 40, 60)
        draw_text("- MOVE RIGHT: 'D' KEY or RIGHT", font, (255, 255, 255), 10, 100)
        draw_text("ARROW KEY", font, (255, 255, 255), 40, 140)
        draw_text("- JUMP: 'W' KEY or UP ARROW KEY", font, (255, 255, 255), 10, 190)
        draw_text("- PAUSE: SPACE BAR", font, (255, 255, 255), 10, 240)
        draw_text("- DIALOGUE: ENTER or MOUSE", font, (255, 255, 255), 10, 290)
        draw_text("- TURN BASED BATTLE: MOUSE", font, (255, 255, 255), 510, 20)
        draw_text("- INSTRUCTIONS: TAB KEY", font, (255, 255, 255), 510, 70)
        draw_text("- RETURN TO GAME SCREEN: PRESS", font, (255, 255, 255), 510, 120)
        draw_text("ESC KEY", font, (255, 255, 255), 540, 160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()
        screen.fill((100, 150, 190))
        clock.tick(FPS)


# levelling system
player_level = 4


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# displays player level on the top left of the screen.
def levels():
    draw_text(f"Level: {player_level}", font, (255, 255, 255), screen, 10, 20)


# this class loads sprite animations and allows the player to interact with
# the bandit (enemy) before leading to the turn_based.py file.
# this class allows the player to move left and right and also jump.
# OOP - inheritance is used.
# lists are used.
# global is only used once.
class Characters(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_frame = 0
        self.attacking = False
        self.attack_frame = 0
        self.attack_counter = 0
        self.goblet = 1
        self.helmet = 1
        self.ring = 1
        self.rose = 1
        self.scroll = 0

        # load all images for the players
        animation_types = ["Idle", "Run", "Attack"]
        for animation in animation_types:
            # reset temp list of images
            mylist = []
            num_of_frames = len(os.listdir(f"/Users/ashleylim/PycharmProjects/NEA project/character animation/{self.char_type}/{animation}"))
            for i in range(num_of_frames-1):
                img = pygame.image.load(f"/Users/ashleylim/PycharmProjects/NEA project/character animation/{self.char_type}/{animation}/{self.char_type}_{animation}_{i+1}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                mylist.append(img)
            self.animation_list.append(mylist)

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, left, right):
        global dx, dy
        dx = 0  # reset movement variables
        dy = 0  # reset movement variables

        if left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx  # update rectangle position
        self.rect.y += dy  # update rectangle position

    def thing(self):
        #encounter = 0
        # update scroll based on player position
        if self.char_type == "player":
            if self.rect.right > GWIDTH - RIGHT_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

                # dialogue starts
                snip = font.render("", True, "white")
                counter = 0
                speed = 3
                active_message = 0
                message = final_dialogue[active_message]

                run = True
                while run:

                    draw_bg()
                    screen.blit(icon, (10, 90))

                    if counter < speed * len(message):
                        counter += 1
                    elif counter >= speed * len(message):
                        pass

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN and active_message < 2 or event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            active_message += 1
                            message = final_dialogue[active_message]
                            counter = 0

                            if active_message == 2:
                                message = final_dialogue[active_message]
                                import fights.final_fight

                    pygame.draw.rect(screen, "black", [0, 200, 990, 200])
                    snip = font.render(message[0:counter//speed], True, "white")
                    screen.blit(snip, (20, 210))

                    pygame.display.update()
                    screen.fill("white")
                    clock.tick(FPS)

            if self.rect.left < LEFT_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

                return screen_scroll

    def animation(self):
        COOLDOWN = 150

        self.image = self.animation_list[self.action][self.index]  # update image depending on current frame

        if pygame.time.get_ticks() - self.update_time > COOLDOWN:  # check if enough time has passed since the last update
            self.update_time = pygame.time.get_ticks()
            self.index += 1

        if self.index >= len(self.animation_list[self.action]):  # if the animation has run out then reset back to the start
            self.index = 0

    def update_action(self, new_action):
        if new_action != self.action:  # check if the new action is different to the previous one
            self.action = new_action
            # update the animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Characters("player", 100, 208, 2, 5)
slime = Characters("bringer-of-death", 725, 147, 2, 5)

UI = UserInterface(player)


while True:

    draw_bg()
    levels()

    # update player actions
    if player.alive:
        if left or right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: idle

        player.move(left, right)
        player.thing()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_TAB:
                instructions()
            if event.key == pygame.K_SPACE:
                # pause

                def draw_text(text, font, color, surface, x, y):
                    text_obj = font.render(text, 1, color)
                    text_rect = text_obj.get_rect()
                    text_rect.topleft = (x, y)
                    surface.blit(text_obj, text_rect)

                # resume button
                def resume():
                    resume_button = pygame.Rect(385, 13, 220, 55)
                    pygame.draw.rect(screen, (150, 1, 0), resume_button)
                    draw_text("RESUME GAME", font, (255, 255, 255), screen, resume_button.left + 17, resume_button.center[1] - 15)

                    return resume_button

                # options button
                def options():
                    options_button = pygame.Rect(385, 78, 220, 55)
                    pygame.draw.rect(screen, (150, 1, 0), options_button)
                    draw_text("OPTIONS", font, (255, 255, 255), screen, options_button.left + 48, options_button.center[1] - 15)

                    return options_button

                # inventory button
                def inventory():
                    inventory_button = pygame.Rect(385, 143, 220, 55)
                    pygame.draw.rect(screen, (150, 1, 0), inventory_button)
                    draw_text("INVENTORY", font, (255, 255, 255), screen, inventory_button.left + 38, inventory_button.center[1] - 15)

                    return inventory_button

                # save button
                def save():
                    save_button = pygame.Rect(385, 208, 220, 55)
                    pygame.draw.rect(screen, (150, 1, 0), save_button)
                    draw_text("SAVE", font, (255, 255, 255), screen, save_button.left + 77, save_button.center[1] - 15)

                    return save_button

                # quit button
                def quit():
                    quit_button = pygame.Rect(385, 273, 220, 55)
                    pygame.draw.rect(screen, (150, 1, 0), quit_button)
                    draw_text("QUIT", font, (255, 255, 255), screen, quit_button.left + 77, quit_button.center[1] - 15)

                    return quit_button

                running = True
                while running:

                    resume_button = resume()
                    options_button = options()
                    inventory_button = inventory()
                    save_button = save()
                    quit_button = quit()

                    click = False
                    x, y = pygame.mouse.get_pos()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                click = True

                    if resume_button.collidepoint((x, y)):
                        pygame.draw.rect(screen, (200, 20, 50), resume_button)
                        draw_text("RESUME GAME", font, (0, 0, 0), screen, resume_button.left + 17, resume_button.center[1] - 15)
                        if click:
                            running = False

                    if options_button.collidepoint((x, y)):
                        pygame.draw.rect(screen, (200, 20, 50), options_button)
                        draw_text("OPTIONS", font, (0, 0, 0), screen, options_button.left + 49, options_button.center[1] - 15)
                        if click:
                            import options.py

                    if inventory_button.collidepoint((x, y)):
                        pygame.draw.rect(screen, (200, 20, 50), inventory_button)
                        draw_text("INVENTORY", font, (0, 0, 0), screen, inventory_button.left + 38, inventory_button.center[1] - 15)
                        if click:
                            UI = UserInterface(player)

                            while running:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:
                                            running = False

                                screen.fill("black")
                                UI.update()
                                UI.render(screen)
                                pygame.display.update()
                                clock.tick(FPS)

                    if save_button.collidepoint((x, y)):
                        pygame.draw.rect(screen, (200, 20, 50), save_button)
                        draw_text("SAVE", font, (0, 0, 0), screen, save_button.left + 77, save_button.center[1] - 15)
                        if click:
                            pass

                    if quit_button.collidepoint((x, y)):
                        pygame.draw.rect(screen, (200, 20, 50), quit_button)
                        draw_text("QUIT", font, (0, 0, 0), screen, quit_button.left + 77, quit_button.center[1] - 15)
                        if click:
                            pygame.quit()

                    pygame.display.update()
                    screen.fill("black")
                    clock.tick(FPS)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right = False

    level.run()
    player.animation()
    player.draw()
    slime.animation()
    slime.draw()
    pygame.display.update()
    screen.fill("grey")
    clock.tick(FPS)
