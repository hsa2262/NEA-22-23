import pygame
from settings.support import import_csv_layout, import_cut_graphics
from settings.settings import tile_size
from tiles.tiles import StaticTile, Lamps, Rock1, Rock2, Sign, Shop


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # lamps
        lamp_layout = import_csv_layout(level_data["lamps"])
        self.lamp_sprites = self.create_tile_group(lamp_layout, "lamps")

        # rock_1
        rock1_layout = import_csv_layout(level_data["rock_1"])
        self.rock1_sprites = self.create_tile_group(rock1_layout, "rock_1")

        # rock_2
        sign_layout = import_csv_layout(level_data["rock_2"])
        self.rock2_sprites = self.create_tile_group(sign_layout, "rock_2")

        # sign
        sign_layout = import_csv_layout(level_data["sign"])
        self.sign_sprites = self.create_tile_group(sign_layout, "sign")

        # shop
        shop_layout = import_csv_layout(level_data["shop"])
        self.shop_sprites = self.create_tile_group(shop_layout, "shop")

    def create_tile_group(self, layout, type):

        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphics("/Users/ashleylim/PycharmProjects/NEA project/background/oak_woods_tileset.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == "lamps":
                        sprite = Lamps(tile_size, x, y)
                        sprite_group.add(sprite)

                    if type == "rock_1":
                        sprite = Rock1(tile_size, x, y)
                        sprite_group.add(sprite)

                    if type == "rock_2":
                        sprite = Rock2(tile_size, x, y)
                        sprite_group.add(sprite)

                    if type == "sign":
                        sprite = Sign(tile_size, x, y)
                        sprite_group.add(sprite)

                    if type == "shop":
                        sprite = Shop(tile_size, x, y)
                        sprite_group.add(sprite)

        return sprite_group

    def run(self):
        # run the entire game / level

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # lamps
        self.lamp_sprites.update(self.world_shift)
        self.lamp_sprites.draw(self.display_surface)

        # rock_1
        self.rock1_sprites.update(self.world_shift)
        self.rock1_sprites.draw(self.display_surface)

        # rock_2
        self.rock2_sprites.update(self.world_shift)
        self.rock2_sprites.draw(self.display_surface)

        # shop
        self.shop_sprites.update(self.world_shift)
        self.shop_sprites.draw(self.display_surface)

        # sign
        self.sign_sprites.update(self.world_shift)
        self.sign_sprites.draw(self.display_surface)
