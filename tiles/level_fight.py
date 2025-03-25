import pygame
from settings.support import import_csv_layout, import_cut_graphics
from settings.settings import tile_size
from tiles.tiles import StaticTile


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        terrain_layout = import_csv_layout(level_data['terrain_fight'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain_fight")

    def create_tile_group(self, layout, type):

        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain_fight":
                        terrain_tile_list = import_cut_graphics("/Users/ashleylim/PycharmProjects/NEA project/background/oak_woods_tileset.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

        return sprite_group

    def run(self):
        # run the entire game / level

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
