from game_init_functions import *
import pygame
import random
from dialogs import Dialog


def game_process_level_3(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()

    map_filename_1 = 'levels/level3_1.txt'
    map_filename_2 = 'levels/level3_2.txt'
    map_filename_3 = 'levels/level3_3.txt'
    map_filename_4 = 'levels/level3_4.txt'
    map_filename_5 = 'levels/level3_5.txt'

    current_map_filename = map_filename_3

    max_x = 10
    max_y = 8

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    doors_group = pygame.sprite.Group()
    dialogs_group = pygame.sprite.Group()
    bells_group = pygame.sprite.Group()
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


    class Bell(pygame.sprite.Sprite):
        bell_image = load_image('world_design/points/bell.png')
        bells_dict = {
            map_filename_1: {
                '1_1': [(1, 0), 'Здесь живет Арбуз'],
                '1_2': [(8, 0), 'Здесь живет Яблоко']
            },
            map_filename_2: {
                '2_1': [(0, 1), 'Здесь живет Тыква'],
                '2_2': [(0, 6), 'Здесь живет Гриб']
            },
            map_filename_4: {
                '4_1': [(9, 1), 'Здесь живет Сова'],
                '4_2': [(9, 6), 'Здесь живет Свекла']
            },
            map_filename_5: {
                '5_1': [(0, 6), 'Здесь живет Осел'],
                '5_2': [(9, 6), 'Здесь живет Шрек']
            }
        }

        def __init__(self, pos_x, pos_y, bell_num):
            super(Bell, self).__init__(all_sprites, bells_group)
            self.pos = (pos_x, pos_y)
            self.image = Bell.bell_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            self.bell_num = bell_num
            self.flag = True

        def update(self):
            player_pos_to_print, text_to_print = Bell.bells_dict[current_map_filename][self.bell_num]

            if player.pos == player_pos_to_print:
                self.tip = Tip(text_to_print)
                self.tip.print_tip()
                self.flag = False
            if player.pos != player_pos_to_print and not self.flag:
                self.tip.clear()
                self.flag = True


    class Player(pygame.sprite.Sprite):
        player_ok_image = load_image('world_design/characters/gold_carrot_ok.png')

        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = Player.player_ok_image
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

    class Door(pygame.sprite.Sprite):
        doors_dict = {'1_1': [map_filename_3, (4, 1)],
                      '2_1': [map_filename_3, (1, 4)],
                      '3_1': [map_filename_1, (4, 6)],
                      '3_2': [map_filename_4, (1, 3)],
                      '3_3': [map_filename_5, (5, 1)],
                      '3_4': [map_filename_2, (8, 4)],
                      '4_1': [map_filename_3, (8, 3)],
                      '5_1': [map_filename_3, (5, 6)]}

        doors_images = {
            'blue_door_right.png': load_image('world_design/doors/blue_door_right.png'),
            'blue_door_left.png': load_image('world_design/doors/blue_door_left.png'),
            'blue_door_up.png': load_image('world_design/doors/blue_door_up.png'),
            'blue_door_down.png': load_image('world_design/doors/blue_door_down.png')
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
            bells_group.empty()
            generate_level(level_map)
            player.move(*end_pos)

    def get_door(door_num):
        result = [elem for elem in doors_group.sprites() if elem.door_num == door_num]
        return result[0] if result else None

    def check_doors():
        door = None
        # дверь 1_1
        if player.pos == (4, 7) and current_map_filename == map_filename_1:
            door = get_door('1_1')
        # дверь 2_1
        if player.pos == (9, 4) and current_map_filename == map_filename_2:
            door = get_door('2_1')
        # дверь 3_1
        elif player.pos == (4, 0) and current_map_filename == map_filename_3:
            door = get_door('3_1')
        # дверь 3_2
        elif player.pos == (9, 3) and current_map_filename == map_filename_3:
            door = get_door('3_2')
        # дверь 3_3
        elif player.pos == (5, 7) and current_map_filename == map_filename_3:
            door = get_door('3_3')
        # дверь 3_4
        elif player.pos == (0, 4) and current_map_filename == map_filename_3:
            door = get_door('3_4')
        # дверь 4_1
        elif player.pos == (0, 3) and current_map_filename == map_filename_4:
            door = get_door('4_1')
        # дверь 5_1
        elif player.pos == (5, 0) and current_map_filename == map_filename_5:
            door = get_door('5_1')

        if door:
            door.go_through_the_door()

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
                elif 'bell' in level[y][x]:
                    bell_num = level[y][x].split('-')[1]
                    Bell(x, y, bell_num)
                else:
                    Tile(level[y][x], x, y)

    possible_to_move_objects = {'.', 'red_point.png', 'blue_door_left.png-3_4', 'dirty_row.png', 'heal.png',
                                'blue_door_right.png-3_2', 'blue_door_down.png-3_3', 'blue_door_up.png-3_1',
                                'blue_door_down.png-1_1', 'blue_door_right.png-2_1', 'blue_door_left.png-4_1',
                                'blue_door_up.png-5_1'}

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

    dialog_with_parrot = Dialog(dialogs_group, 'data/dialogs/dialog6.txt')
    dialog1_started = False
    dialog_with_beet1 = Dialog(dialogs_group, 'data/dialogs/dialog7.txt')
    dialog2_started = False
    dialog_with_melon = Dialog(dialogs_group, 'data/dialogs/dialog8.txt')
    dialog3_started = False
    dialog_with_pumpkin1 = Dialog(dialogs_group, 'data/dialogs/dialog9.txt')
    dialog4_started = False
    dialog_with_pumpkin2 = Dialog(dialogs_group, 'data/dialogs/dialog10.txt')
    dialog5_started = False
    dialog_with_beet2 = Dialog(dialogs_group, 'data/dialogs/dialog11.txt')
    dialog6_started = False
    dialog_with_apple = Dialog(dialogs_group, 'data/dialogs/dialog12.txt')
    dialog7_started = False

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    screen.fill((0, 0, 0))

    while True:  # главный игровой цикл
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
                if dialog1_started and player.pos == (4, 3) and\
                        current_map_filename == map_filename_3:
                    if dialog_with_parrot.check_start_dialog():
                        dialog_with_parrot.next_string(screen)

                if dialog2_started and player.pos == (4, 3) and\
                        current_map_filename == map_filename_4:
                    if dialog_with_beet1.check_start_dialog():
                        dialog_with_beet1.next_string(screen)

        if player.pos == (4, 3) and not dialog1_started and current_map_filename == map_filename_3:
            dialog_with_parrot.next_string(screen)
            dialog1_started = True



        check_doors()

        tiles_group.draw(screen)
        doors_group.draw(screen)
        bells_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        bells_group.update()
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 900)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_3(screen)
