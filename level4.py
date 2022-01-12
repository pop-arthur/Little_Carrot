from game_init_functions import *
import pygame
import random
from dialogs import Dialog


def game_process_level_4(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()

    map_filename_1 = 'levels/level4.txt'
    current_map_filename = map_filename_1

    max_x = 10
    max_y = 8

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    dialogs_group = pygame.sprite.Group()
    tip_grooup = pygame.sprite.Group()

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
                       'Stone-1.png': [load_image('world_design/Stones/Stone-1.png', scale_size=(74, 90)), (13, 10)],
                       'red_point.png': [load_image('world_design/points/red_point.png'), (0, 0)],
                       'dirty_row.png': [load_image('world_design/Ground/dirty_row.png'), (0, 0)],
                       'parrot': [load_image('world_design/characters/parrot.png'), (0, 0)],
                       'apple.png': [load_image('world_design/characters/apple.png'), (0, 0)],
                       'beet.png': [load_image('world_design/characters/beet.png'), (0, 0)],
                       'pumpkin.png': [load_image('world_design/characters/pumpkin.png'), (0, 0)],
                       'watermelon.png': [load_image('world_design/characters/watermelon.png'), (0, 0)],
                       'dog.png': [load_image('world_design/characters/dog.png'), (0, 0)],
                       'scarecrow.png': [load_image('world_design/characters/scarecrow.png', scale_size=(90, 90)), (5, 5)],
                       'Sculture-2.png': [load_image('world_design/Sculptures/Sculture-2.png'), (0, 0)],
                       'Sculpture-1.png': [load_image('world_design/Sculptures/Sculpture-1.png'), (0, 0)],
                       'box.png': [load_image('world_design/Stones/box.png'), (0, 0)],
                       'light_earth.png': [load_image('world_design/Ground/light_earth.png'), (0, 0)],
                       'Tree-1-4.png': [load_image('world_design/Trees/Tree-1/Tree-1-4.png'), (0, 0)],
                       'portal.png': [load_image('world_design/points/portal.png'), (0, 0)],
                       'heal.png': [load_image('world_design/points/heal.png'), (0, 0)],
                       'Flower-3.png': [load_image('world_design/Flowers/Flower-3.png'), (0, 0)]}

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
            elif self.tile_type == 'heal.png':
                if player.pos == self.pos:
                    player.heal(1)
                    tiles_group.remove(self)

    class Tip(pygame.sprite.Sprite):
        def __init__(self, text):
            super().__init__(tip_grooup)
            self.text = text
            self.font = pygame.font.Font(None, 35)
            self.output_text = self.font.render(self.text, True, (255, 255, 255))
            self.place = self.output_text.get_rect(center=(500, 850))

        def print_tip(self):
            self.clear()
            self.output_text = self.font.render(self.text, True, (255, 255, 255))
            self.place = self.output_text.get_rect(center=(500, 850))
            screen.blit(self.output_text, self.place)

        def clear(self):
            self.output_text.fill((0, 0, 0))
            screen.blit(self.output_text, self.place)

    class Player(pygame.sprite.Sprite):
        player_with_gun_image = load_image('world_design/characters/gold_carrot_with_gun.png')

        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = Player.player_with_gun_image
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

        def damage(self, count_of_damage):
            print('Вас ударило')

        def heal(self, count_of_heal):
            print('Подлечились!')

    def generate_level(level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                Tile('empty', x, y)
                if level[y][x] == '.':
                    pass
                else:
                    Tile(level[y][x], x, y)

    possible_to_move_objects = {'.', 'red_point.png', 'blue_door_left.png-3_4', 'dirty_row.png', 'heal.png',
                                'blue_door_right.png-3_2', 'blue_door_down.png-3_3', 'blue_door_up.png-3_1',
                                'blue_door_down.png-1_1', 'blue_door_right.png-2_1', 'blue_door_left.png-4_1',
                                'blue_door_up.png-5_1', 'portal.png'}

    def move(movement):
        nonlocal level_map, player
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

        # положение на карте
        change_player_pos_on_map(current_map_filename, player.pos)
        # грядки
        if level_map[player.pos[1]][player.pos[0]] == 'dirty_row.png':
            player.damage(1)

    dialog_status = False
    dialog_with_dog1 = Dialog(dialogs_group, 'data/dialogs/dialog13.txt', (7, 6))
    dialog1_started = False
    dialog_with_dog2 = Dialog(dialogs_group, 'data/dialogs/dialog14.txt', (7, 6))
    dialog2_started = False

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    screen.fill((0, 0, 0))

    running = True
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move("up")
                if event.key == pygame.K_a:
                    move("left")
                if event.key == pygame.K_s:
                    move("down")
                if event.key == pygame.K_d:
                    move("right")

            if event.type == pygame.MOUSEBUTTONUP:
                if dialog1_started and dialog_with_dog1.check_position(player.pos, screen):
                    if dialog_with_dog1.check_start_dialog():
                        dialog_with_dog1.next_string(screen)

                if dialog2_started and dialog_with_dog2.check_position(player.pos, screen):
                    if dialog_with_dog2.check_start_dialog():
                        dialog_with_dog2.next_string(screen)

        if dialog_with_dog1.check_position(player.pos, screen) and not dialog1_started:
            dialog1_started = True
            dialog_with_dog1.next_string(screen)

        #Второй диалог после учения
        #if dialog_with_dog2.check_position(player.pos, screen) and not dialog2_started:
            #dialog2_started = True
            #dialog_with_dog2.next_string(screen)

        if not dialog_with_dog2.check_start_dialog():
            print('Конец уровня')

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
    game_process_level_4(screen)
