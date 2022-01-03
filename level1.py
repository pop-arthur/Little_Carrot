import os
import random
import sys
import pygame
from game_init_functions import *


def game_process_level_1(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()

    map_filename = 'levels/level1_1.txt'

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(all_sprites, tiles_group)

            image, indent = tile_images[tile_type]
            indent_x, indent_y = indent

            if tile_type == "empty":
                self.image = load_image(f"world_design/Ground/Dark-grass-{random.randint(1, 4)}.png")
            else:
                self.image = image

            self.rect = self.image.get_rect().move(
                tile_width * pos_x + indent_x, tile_height * pos_y + indent_y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = player_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 5, tile_height * pos_y)
            self.pos = (pos_x, pos_y)

        def move(self, x, y):
            self.pos = (x, y)
            self.rect = self.image.get_rect().move(
                tile_width * x + 5, tile_height * y)

    class Portal(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, n_frames):
            super(Portal, self).__init__(all_sprites, tiles_group)
            self.frames = [load_image(f"world_design/Portal/Portal-{i}.png") for i in range(1, 4)]
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.n_frames = n_frames

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % (len(self.frames) * self.n_frames)
            self.image = self.frames[self.cur_frame // self.n_frames]

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    tile_images = {'empty': ['', (0, 0)],
                   'Bush-4.png': [load_image('world_design/Bushes/Bush-4.png', scale_size=(74, 74)), (13, 35)],
                   'Big-wooden-fence-1.png':
                       [load_image('world_design/Fences/Big wooden fence/Big-wooden-fence-1.png', scale_size=(100, 75)),
                        (0, 25)],
                   'Big-wooden-fence-2.png':
                       [load_image('world_design/Fences/Big wooden fence/Big-wooden-fence-2.png', scale_size=(100, 75)),
                        (0, 25)],
                   'Big-wooden-fence-3.png':
                       [load_image('world_design/Fences/Big wooden fence/Big-wooden-fence-3.png', scale_size=(100, 75)),
                        (0, 25)],
                   'parrot': [load_image('world_design/characters/parrot.png'), (0, 0)],
                   'Stone-1.png': [load_image('world_design/Stones/Stone-1.png'), (0, 0)]}
    player_image = load_image('world_design/gold_carrot_ok.png')

    def generate_level(level):
        new_player, x, y = None, None, None
        print(level)
        for y in range(len(level)):
            for x in range(len(level[y])):
                Tile('empty', x, y)
                if level[y][x] == '.':
                    pass
                elif level[y][x] == 'carrot':
                    new_player = Player(x, y)
                else:
                    Tile(level[y][x], x, y)

        # вернем игрока, а также размер поля в клетках
        return new_player, len(level[0]), len(level)

    def move(player, movement):
        global level_map
        level_map = load_level(map_filename)

        print(level_map)

        x, y = pos_before = player.pos
        if movement == "up":
            if y > 0 and level_map[y - 1][x] == ".":
                player.move(x, y - 1)
        if movement == "down":
            if y < max_y and level_map[y + 1][x] == ".":
                player.move(x, y + 1)
        if movement == "left":
            if x > 0 and level_map[y][x - 1] == ".":
                player.move(x - 1, y)
        if movement == "right":
            if x < max_x and level_map[y][x + 1] == ".":
                player.move(x + 1, y)

        change_player_pos_on_map(map_filename, pos_before, player.pos)
        level_map = load_level(map_filename)

    level_map = load_level(map_filename)
    player, max_x, max_y = generate_level(level_map)

    for i in range(256):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        screen.fill((i,) * 3)
        pygame.display.flip()
        clock.tick(FPS)

    while True:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(player, "up")
                if event.key == pygame.K_a:
                    move(player, "left")
                if event.key == pygame.K_s:
                    move(player, "down")
                if event.key == pygame.K_d:
                    move(player, "right")

        screen.fill(pygame.Color("black"))
        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        draw_lines(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 900)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_1(screen)