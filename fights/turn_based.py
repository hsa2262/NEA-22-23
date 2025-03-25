import pygame, sys
from settings.settings import *
from tiles.level_fight import Level
from tiles.game_data import level_0
import random
import settings.button

# dialogue telling players to check inventory
with open(r"/Users/ashleylim/PycharmProjects/NEA project/dialogue_text.txt", 'r') as fp:
    # lines to read
    line_numbers = [28, 29, 30, 31]
    # To store lines
    check_inventory = []
    for i, line in enumerate(fp):
        if i in line_numbers:
            check_inventory.append(line.strip())

# screen
pygame.init()
screen = pygame.display.set_mode((GWIDTH, PHEIGHT + bottom_panel))
clock = pygame.time.Clock()
pygame.display.set_caption("NEA project")
font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 32)
other_font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/pixelmix.ttf", 54)
level = Level(level_0, screen)
scroll = 0
icon = pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/images/icon.png").convert_alpha()
icon = pygame.transform.scale(icon, (30 * 5, 22 * 5))
exp_received = 0


# game variables
current_fighter = 1
total_fighters = 2
cooldown = 0
wait_time = 100
attack_key = False
game_over = 0

screen = pygame.display.set_mode((GWIDTH, PHEIGHT + bottom_panel))

# button images
heal_img = pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/heal.png").convert_alpha()
attack_img = pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/attack.png").convert_alpha()


# this class loads sprite animation and changes the number of items in the
# inventory.
# OOP - inheritance is used.
# lists are used.
# this class allows the player to restart the fight if they lose.
class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, max_hp, strength, heal):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_frame = 0
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.heal = heal
        self.alive = True
        self.goblet = 1

        animation_types = ["Idle", "Attack", "Death"]
        enemy_idle = "/Users/ashleylim/PycharmProjects/NEA project/character animation/Bringer-Of-Death/Idle"

        mylist = []
        for i in range(5):
            img = pygame.image.load(f"/Users/ashleylim/PycharmProjects/NEA project/character animation/{self.char_type}/Idle/{self.char_type}_Idle_{i+1}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            mylist.append(img)
        self.animation_list.append(mylist)

        mylist = []
        for i in range(8):
            img = pygame.image.load(f"/Users/ashleylim/PycharmProjects/NEA project/character animation/{self.char_type}/Attack/{self.char_type}_Attack_{i+1}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            mylist.append(img)
        self.animation_list.append(mylist)

        mylist = []
        for i in range(8):
            img = pygame.image.load(f"/Users/ashleylim/PycharmProjects/NEA project/character animation/{self.char_type}/Death/{self.char_type}_Death_{i+1}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            mylist.append(img)
        self.animation_list.append(mylist)

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def animation(self):
        COOLDOWN = 140

        self.image = self.animation_list[self.action][self.index]  # update image depending on current frame

        if pygame.time.get_ticks() - self.update_time > COOLDOWN:  # check if enough time has passed since the last update
            self.update_time = pygame.time.get_ticks()
            self.index += 1

        if self.index >= len(self.animation_list[self.action]):  # if the animation has run out then reset back to the start
            if self.action == 2:
                self.index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    def update_action(self, new_action):
        if new_action != self.action:  # check if the new action is different to the previous one
            self.action = new_action
            # update the animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # damage enemy
        num = random.randint(-5, 5)
        dmg = self.strength + num
        target.hp -= dmg
        # check if ded
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        dmg_txt = DmgText(target.rect.centerx, target.rect.y, str(dmg), (255, 0, 0))
        dmg_txt_grp.add(dmg_txt)
        # attack animation
        self.action = 1
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

    def death(self):
        self.action = 2
        self.index = 0
        self.update_time = pygame.time.get_ticks()

    def restart(self):
        self.alive = True
        self.hp = self.max_hp
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


# this class is for the player and enemy health.
# their HP (health points) are displayed on the screen.
class Health:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        # health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 160, 30))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 160 * ratio, 30))


# this class is for the sprite damage.
class DmgText(pygame.sprite.Sprite):
    def __init__(self, x, y, dmg, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(dmg, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


dmg_txt_grp = pygame.sprite.Group()

enemy = Character("Slime", 750, 200, 4, 30, 6, 1)
player = Character("player", 250, 197, 4, 25, 10, 3)

# player and enemy health
player_health = Health(160, PHEIGHT - bottom_panel + 270, player.hp, player.max_hp)
enemy_health = Health(650, PHEIGHT - bottom_panel + 270, enemy.hp, enemy.max_hp)

# button thing
attack_button = settings.button.Button(screen, 180, PHEIGHT - bottom_panel + 310, attack_img, 48, 48)
heal_button = settings.button.Button(screen, 250, PHEIGHT - bottom_panel + 310, heal_img, 48, 48)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# background
bg_images = []
for i in range(1, 4):
    bg_image = pygame.image.load(f"/Users/ashleylim/PycharmProjects/NEA project/background/background_layer_{i}.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (320 * 1.5, 180 * 1.5))
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


def draw_bg():
    for x in range(5):
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll, 0))


running = True
while running:
    draw_bg()
    draw_text(f"{player.char_type} HP: {player.hp}", font, (255, 255, 255), 140, PHEIGHT - bottom_panel + 230)
    draw_text(f"{enemy.char_type} HP: {enemy.hp}", font, (255, 255, 255), 630, PHEIGHT - bottom_panel + 230)
    player_health.draw(player.hp)
    enemy_health.draw(enemy.hp)

    player.update()
    enemy.update()

    dmg_txt_grp.update()
    dmg_txt_grp.draw(screen)

    attack = False
    heal = False
    heal_effect = 4

    if heal_button.draw():
        heal = True

    if attack_button.draw():
        attack = True

    if game_over == 0:
        # player
        if player.alive:
            if current_fighter == 1:
                cooldown += 1
                if cooldown >= wait_time:
                    if attack:
                        player.attack(enemy)
                        current_fighter += 1
                        cooldown = 0
                    if heal:
                        if player.heal > 0:
                            if player.max_hp - player.hp > heal_effect:
                                heal_amount = heal_effect
                            else:
                                heal_amount = player.max_hp - player.hp
                            player.hp += heal_amount
                            dmg_txt = DmgText(player.rect.centerx, player.rect.y, str(heal_amount), (0, 255, 0))
                            dmg_txt_grp.add(dmg_txt)
                            current_fighter += 1
                            cooldown = 0
        else:
            game_over = -1

        # enemy
        if current_fighter == 2:
            if enemy.alive:
                cooldown += 1
                if cooldown >= wait_time:
                    # check if enemy needs healing
                    if (enemy.hp / enemy.max_hp) < 0.3:
                        if enemy.max_hp - enemy.hp > heal_effect:
                            heal_amount = heal_effect
                        else:
                            heal_amount = enemy.max_hp - enemy.hp
                        enemy.hp += heal_amount
                        dmg_txt = DmgText(enemy.rect.centerx, enemy.rect.y, str(heal_amount), (0, 255, 0))
                        dmg_txt_grp.add(dmg_txt)
                        current_fighter += 1
                        cooldown = 0
                    else:
                        enemy.attack(player)
                        current_fighter += 1
                        cooldown = 0
            else:
                game_over = 1

        if current_fighter > total_fighters:
            current_fighter = 1

    # check if game over
    if game_over != 0:
        if game_over == 1:
            draw_text("VICTORY", other_font, (0, 255, 0), 365, PHEIGHT - bottom_panel - 50)
            draw_text("Press E to continue", font, (0, 0, 0), 340, PHEIGHT - bottom_panel + 30)

        if game_over == -1:
            draw_text("DEFEAT", other_font, (255, 0, 0), 365, PHEIGHT - bottom_panel - 50)
            draw_text("Press R to restart", font, (0, 0, 0), 340, PHEIGHT - bottom_panel + 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # if e is pressed, dialogue will appear
                running = False
                screen = pygame.display.set_mode((GWIDTH, GHEIGHT))
                snip = font.render("", True, "white")
                counter = 0
                speed = 3
                active_message = 0
                message = check_inventory[active_message]

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
                        if event.type == pygame.MOUSEBUTTONDOWN and active_message < 3 or event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            active_message += 1
                            message = check_inventory[active_message]
                            counter = 0
                            print("m:", message)
                            print(active_message)

                            if active_message == 3:
                                message = check_inventory[active_message]
                                run = False

                    pygame.draw.rect(screen, "black", [0, 200, 990, 200])

                    snip = font.render(message[0:counter//speed], True, "white")
                    screen.blit(snip, (20, 210))

                    pygame.display.update()
                    screen.fill("white")
                    clock.tick(FPS)

                import enemy_encounters.enemy_encounter2

            if event.key == pygame.K_r:
                player.restart()
                enemy.restart()
                current_fighter = 1
                cooldown = 140
                game_over = 0

    level.run()
    player.animation()
    enemy.animation()
    player.draw()
    enemy.draw()
    pygame.display.update()
    screen.fill("black")
    clock.tick(FPS)

