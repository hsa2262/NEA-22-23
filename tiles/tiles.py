import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

    def scale(self, scale, size):
        pic = pygame.transform.scale(self.image, (size * scale, size * scale))
        return pic

    def scale_v(self, scale):
        img = pygame.transform.scale(self.image, (23 * scale, 57 * scale))
        return img


class Lamps(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/background/lamp.png").convert_alpha())
        self.image = self.scale_v(1.5)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Rock1(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/background/rock_1.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Rock2(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/background/rock_2.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Sign(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/background/sign.png").convert_alpha())
        self.image = self.scale(3, size)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Shop(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("/Users/ashleylim/PycharmProjects/NEA project/background/shop.png").convert_alpha())
        self.image = self.scale(8, size)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

