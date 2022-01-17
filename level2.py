import time

from game_init_functions import *
from db_functions import *
import pygame
import random
from dialogs import Dialog
from credits import death_screen
from health_output import Health_Output


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

    egg_group = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    success = True

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
                       'potato': [load_image('world_design/characters/potato.png'), (0, 0)],
                       'Stone-1.png': [load_image('world_design/Stones/Stone-1.png', scale_size=(74, 90)), (13, 10)],
                       'red_point.png': [load_image('world_design/points/red_point.png'), (0, 0)],
                       'dirty_row.png': [load_image('world_design/Ground/dirty_row.png'), (0, 0)],
                       'Sculture-2.png': [load_image('world_design/Sculptures/Sculture-2.png'), (0, 0)],
                       'box.png': [load_image('world_design/Stones/box.png'), (0, 0)],
                       'light_earth.png': [load_image('world_design/Ground/light_earth.png'), (0, 0)],
                       'Tree-1-4.png': [load_image('world_design/Trees/Tree-1/Tree-1-4.png'), (0, 0)],
                       'portal.png': [load_image('world_design/points/portal.png'), (0, 0)]}

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
        player_ok_image = load_image('world_design/characters/gold_carrot_ok.png')
        player_flattened_image = load_image('world_design/characters/gold_carrot_flattened.png')

        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = Player.player_ok_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 5, tile_height * pos_y)
            self.pos = (pos_x, pos_y)
            self.hp = get_current_hp()

        def move(self, x, y):
            self.pos = (x, y)
            self.rect = self.image.get_rect().move(
                tile_width * x + 5, tile_height * y)

        def check_parrot(self):
            if self.pos == (4, 2):
                return True
            return False

        def be_flattened(self):
            self.image = Player.player_flattened_image

        def be_ok(self):
            self.image = Player.player_ok_image

        def damage(self, count_of_damage):
            damage_sound.play()
            self.hp -= count_of_damage
            if self.hp <= 0:
                nonlocal success
                death_screen(screen)
                success = False

        def heal(self, count_of_heal):
            self.hp += count_of_heal

    class Door(pygame.sprite.Sprite):
        doors_dict = {'1_1': [map_filename_2, (0, 4)],
                      '2_1': [map_filename_3, (0, 4)],
                      '3_1': [map_filename_2, (9, 4)]}
        doors_images = {
            'blue_door_right.png': load_image('world_design/doors/blue_door_right.png'),
            'blue_door_left.png': load_image('world_design/doors/blue_door_left.png')
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

    possible_to_move_objects = {'.', 'red_point.png', 'blue_door_right.png-1_1', 'dirty_row.png'}

    def move(player, movement):
        nonlocal level_map
        level_map = load_level(current_map_filename)[0]

        if swap_control:
            if movement == "up":
                movement = "down"
            elif movement == "down":
                movement = "up"
            elif movement == "left":
                movement = "right"
            elif movement == "right":
                movement = "left"

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

        # грядки
        if level_map[player.pos[1]][player.pos[0]] == 'dirty_row.png':
            player.damage(1)

    class Egg(pygame.sprite.Sprite):
        egg_image = load_image('world_design/characters/egg.png', scale_size=(50, 80))

        def __init__(self, count_of_hits):
            super().__init__(all_sprites, egg_group)
            self.image = Egg.egg_image
            self.rect = self.image.get_rect().move(600, 500)
            speeds = [-4, -3, -2, 2, 3, 4]
            self.vx = random.choice(speeds)
            self.vy = random.choice(speeds)
            self.counter = count_of_hits

        def update(self):

            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
                self.counter -= 1
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
                self.counter -= 1

            if pygame.sprite.spritecollideany(self, player_group):
                player.damage(1)
                self.vx = -self.vx
                self.vy = -self.vy
                self.kill()
            if self.counter == 0:
                self.kill()

    class Border(pygame.sprite.Sprite):
        # строго вертикальный или строго горизонтальный отрезок
        def __init__(self, x1, y1, x2, y2):
            super().__init__(all_sprites)
            if x1 == x2:  # вертикальная стенка
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:  # горизонтальная стенка
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def creating_second_door():
        nonlocal second_door_is_active, create_second_door
        Door(9, 4, '2_1', 'blue_door_right.png')
        second_door_is_active = True
        create_second_door = False

    def creating_third_door():
        nonlocal third_door_is_active
        Door(0, 4, '3_1', 'blue_door_left.png')
        third_door_is_active = True

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    player.be_flattened()
    generate_level(level_map)

    dialog_with_parrot = Dialog(dialogs_group, 'data/dialogs/dialog3.txt', (4, 2))
    dialog_with_potato1 = Dialog(dialogs_group, 'data/dialogs/dialog4.txt', (8, 3))
    dialog_with_potato2 = Dialog(dialogs_group, 'data/dialogs/dialog5.txt', (8, 3))

    eggs_started = False
    for i in range(9):
        Egg(4)

    Border(1, 1, 999, 1)
    Border(1, 799, 999, 799)
    Border(1, 1, 1, 799)
    Border(999, 1, 999, 799)

    screen.fill((0, 0, 0))
    save_level(2)

    first_dialog_started = False
    swap_control = True
    create_second_door = True
    second_door_is_active = False
    second_dialog1_started = False
    second_dialog2_started = False
    third_door_is_active = False
    portal_is_active = False
    end_transformation = False

    health_string = Health_Output(screen, (500, 825), player.hp)

    damage_sound = pygame.mixer.Sound('data/music/damage_sound_full.mp3')
    damage_sound.set_volume(0.5)

    pygame.mixer.music.load('data/music/main_sound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.04)

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

                if event.key == pygame.K_h and event.mod & pygame.KMOD_LCTRL:
                    player.heal(8)

            if event.type == pygame.MOUSEBUTTONUP:
                if player.pos == (4, 2) and first_dialog_started and\
                        current_map_filename == map_filename_1:
                    if dialog_with_parrot.check_start_dialog():
                        dialog_with_parrot.next_string(screen)

                if player.pos == (8, 3) and second_dialog1_started and \
                        current_map_filename == map_filename_3:
                    if dialog_with_potato1.check_start_dialog():
                        dialog_with_potato1.next_string(screen)

                if player.pos == (8, 3) and second_dialog2_started and \
                        current_map_filename == map_filename_3:
                    if dialog_with_potato2.check_start_dialog():
                        dialog_with_potato2.next_string(screen)

        if not success:
            return False

        # старт диалога 1
        if not first_dialog_started and player.pos == (4, 2) and current_map_filename == map_filename_1:
            if dialog_with_parrot.check_start_dialog():
                dialog_with_parrot.next_string(screen)
                first_dialog_started = True

        # дверь 1
        if level_map[player.pos[1]][player.pos[0]] == 'blue_door_right.png-1_1' and \
                current_map_filename == map_filename_1:
            door = get_door('1_1')
            if door:
                door.go_through_the_door()
                eggs_started = True

        # дверь 2
        if second_door_is_active and player.pos == (9, 4):
            door = get_door('2_1')
            door.go_through_the_door()
            all_sprites.remove(door)
            doors_group.remove(door)
            second_door_is_active = False

        # дверь 3
        if player.pos == (0, 4) and current_map_filename == map_filename_3 and third_door_is_active:
            door = get_door('3_1')
            door.go_through_the_door()
            all_sprites.remove(door)
            doors_group.remove(door)
            third_door_is_active = False
            portal_is_active = True
            Tile('portal.png', 4, 3)

        # портал:
        if portal_is_active and player.pos == (4, 3) and current_map_filename == map_filename_2:
            break

        # диалог 2
        if not dialog_with_potato1.check_start_dialog() and end_transformation and not second_dialog2_started:
            dialog_with_potato2.next_string(screen)
            second_dialog2_started = True

        if level_map[player.pos[1]][player.pos[0]] == 'red_point.png' and \
            current_map_filename == map_filename_3:
            if dialog_with_potato1.check_start_dialog() and not second_dialog1_started:
                dialog_with_potato1.next_string(screen)
                second_dialog1_started = True

            if not dialog_with_potato1.check_start_dialog() and not second_dialog2_started:
                for _ in range(300):
                    screen.fill((random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)))
                    clock.tick(FPS)
                    pygame.display.flip()
                screen.fill((0, 0, 0))
                player.be_ok()
                end_transformation = True



            if not dialog_with_potato2.check_start_dialog() and swap_control:
                swap_control = False
                creating_third_door()

        tiles_group.draw(screen)
        doors_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        draw_lines(screen)

        if eggs_started:
            if create_second_door:
                creating_second_door()

            horizontal_borders.draw(screen)
            vertical_borders.draw(screen)
            egg_group.draw(screen)
            egg_group.update()

        health_string.update_hp(screen, player.hp)

        pygame.display.flip()
        clock.tick(FPS)

    set_hp(player.hp)
    return True


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 950)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_2(screen)
