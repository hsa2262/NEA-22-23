import pygame
# this file uses OOP.


# this class creates slots where items will be placed into.
class InventorySlot:
    def __init__(self, name, pos):
        self.image = pygame.image.load(name)
        self.image = pygame.transform.scale(self.image, (16*4, 16*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = 0
        self.font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 34)

    def render(self, display):
        text = self.font.render(str(self.count), True, (0, 0, 0))
        display.blit(self.image, self.rect)
        display.blit(text, self.rect.midright)


# this is the user interface of the inventory.
class UserInterface:
    def __init__(self, player):
        self.font = pygame.font.Font("/Users/ashleylim/PycharmProjects/NEA project/images/fonts/FreePixel.ttf", 34)
        self.inventory = Inventory(player)

    def update(self):
        self.inventory.update()

    def render(self, display):
        self.inventory.render(display)


# this class puts all the items into the inventory, including:
# goblet, helmet, ring, rose and scroll.

class Inventory:
    def __init__(self, player):
        self.slots = []
        self.count = 0

        self.image = pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/images/inventory.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (127*4.75, 69*4.75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 5)

        self.playerinfo = player

        self.slots.append(InventorySlot("/Users/ashleylim/PycharmProjects/NEA project/images/items/goblet.png", (230, 50)))
        self.slots.append(InventorySlot("/Users/ashleylim/PycharmProjects/NEA project/images/items/helmet.png", (325, 45)))
        self.slots.append(InventorySlot("/Users/ashleylim/PycharmProjects/NEA project/images/items/ring.png", (420, 50)))
        self.slots.append(InventorySlot("/Users/ashleylim/PycharmProjects/NEA project/images/items/rose.png", (505, 50)))
        self.slots.append(InventorySlot("/Users/ashleylim/PycharmProjects/NEA project/images/items/scroll.png", (590, 50)))

    def update(self):
        self.slots[0].count = self.playerinfo.goblet
        self.slots[1].count = self.playerinfo.helmet
        self.slots[2].count = self.playerinfo.ring
        self.slots[3].count = self.playerinfo.rose
        self.slots[4].count = self.playerinfo.scroll

    def render(self, display):
        display.blit(self.image, self.rect)
        for i in self.slots:
            i.render(display)
