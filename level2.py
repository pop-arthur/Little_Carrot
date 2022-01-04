from game_init_functions import *
import pygame
import random
from dialogs import Dialog


def game_process_level_2(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()

    map_filename_1 = 'levels/level2_1.txt'
    map_filename_2 = 'levels/level2_2.txt'
    map_filename_3 = 'levels/level2_3.txt'

    current_map_filename = map_filename_1

    max_x = 10
    max_y = 8

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    doors_group = pygame.sprite.Group()
    dialogs_group = pygame.sprite.Group()

    class Tile(pygame.sprite.Sprite):
        tile_images = {'empty': ['', (0, 0)],
                       'Bush-4.png': [load_image('world_design/Bushes/Bush-4.png', scale_size=(74, 74)), (13, 35)],
                       'Big-wooden-fence-1.png':
                           [load_image('world_design/Fences/Big wooden fence/Big-wooden-fence-1.png',
                                       scale_size=(100, 75)),
                            (0, 25)],
                       'Big-wooden-fence-2.png':
                           [load_image('world_design/Fences/Big wooden fence/Big-wooden-fence-2.png',
                                       scale_size=(100, 75)),
                            (0, 25)],
                       'Big-wooden-fence-3.png':
                           [load_image('world_design/Fences/Big wooden fence/Big-wooden-fence-3.png',
                                       scale_size=(100, 75)),
                            (0, 25)],
                       'parrot': [load_image('world_design/characters/parrot.png'), (0, 0)],
                       'Stone-1.png': [load_image('world_design/Stones/Stone-1.png', scale_size=(74, 90)), (13, 10)],
                       'red_point.png': [load_image('world_design/points/red_point.png'), (0, 0)]}

        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(all_sprites, tiles_group)

            self.tile_type = tile_type
            self.pos = (pos_x, pos_y)
            image, indent = Tile.tile_images[tile_type]
            indent_x, indent_y = indent

            if tile_type == "empty":
                self.image = load_image(f"world_design/Ground/Dark-grass-{random.randint(1, 4)}.png")
            else:
                self.image = image

            self.rect = self.image.get_rect().move(
                tile_width * pos_x + indent_x, tile_height * pos_y + indent_y)

        def update(self, *args):
            if self.tile_type == 'red_point.png':
                if player.pos == self.pos:
                    tiles_group.remove(self)

    class Player(pygame.sprite.Sprite):
        player_image = load_image('world_design/gold_carrot_ok.png')

        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = Player.player_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 5, tile_height * pos_y)
            self.pos = (pos_x, pos_y)

        def move(self, x, y):
            self.pos = (x, y)
            self.rect = self.image.get_rect().move(
                tile_width * x + 5, tile_height * y)

        def check_parrot(self):
            if self.pos == (4, 2):
                return True
            return False

    class Door(pygame.sprite.Sprite):
        doors_dict = {'1_1': [map_filename_2, (0, 4)]}
        doors_images = {
            'blue_door_right.png': load_image('world_design/doors/blue_door_right.png')
        }

        def __init__(self, pos_x, pos_y, door_num, door_type):
            super().__init__(all_sprites, doors_group)

            self.pos = (pos_x, pos_y)
            self.door_num = door_num
            self.image = Door.doors_images[door_type]

            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

        def go_through_the_door(self):
            nonlocal current_map_filename, level_map, player_pos, player
            end_map, end_pos = Door.doors_dict[self.door_num]
            change_player_pos_on_map(current_map_filename, (-1, -1))
            current_map_filename = end_map
            change_player_pos_on_map(current_map_filename, end_pos)
            level_map, player_pos = load_level(current_map_filename)
            tiles_group.empty()
            doors_group.empty()
            generate_level(level_map)
            player.move(*end_pos)

    def get_door(door_num):
        result = [elem for elem in doors_group.sprites() if elem.door_num == door_num]
        return result[0] if result else None

    def generate_level(level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                Tile('empty', x, y)
                if level[y][x] == '.':
                    pass
                elif 'door' in level[y][x]:
                    door_type = level[y][x].split('-')[0]
                    door_num = level[y][x].split('-')[1]
                    Door(x, y, door_num, door_type)
                else:
                    Tile(level[y][x], x, y)

    possible_to_move_objects = {'.', 'red_point.png', 'blue_door_right.png-1_1'}

    def move(player, movement):
        nonlocal level_map
        level_map = load_level(current_map_filename)[0]

        x, y = player.pos
        if movement == "up":
            if y > 0 and level_map[y - 1][x] in possible_to_move_objects:
                player.move(x, y - 1)
        if movement == "down":
            if y < max_y - 1 and level_map[y + 1][x] in possible_to_move_objects:
                player.move(x, y + 1)
        if movement == "left":
            if x > 0 and level_map[y][x - 1] in possible_to_move_objects:
                player.move(x - 1, y)
        if movement == "right":
            if x < max_x - 1 and level_map[y][x + 1] in possible_to_move_objects:
                player.move(x + 1, y)

        change_player_pos_on_map(current_map_filename, player.pos)

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    dialog_with_parrot = Dialog(dialogs_group, 'data/dialogs/dialog3.txt')

    screen.fill((0, 0, 0))
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

            if event.type == pygame.MOUSEBUTTONUP:

                if level_map[player.pos[1]][player.pos[0]] == 'red_point.png' and current_map_filename == map_filename_1:
                    if dialog_with_parrot.check_start_dialog():
                        dialog_with_parrot.next_string(screen)

        if level_map[player.pos[1]][player.pos[0]] == 'blue_door_right.png-1_1':
            door = get_door('1_1')
            if door:
                door.go_through_the_door()
                # начало яиц

        tiles_group.draw(screen)
        doors_group.draw(screen)
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
    game_process_level_2(screen)
