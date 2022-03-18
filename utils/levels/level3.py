from utils.game_functions.game_init_functions import *
from utils.db.db_functions import *
import pygame
import random
from utils.secondary_functions.dialogs import Dialog
from utils.secondary_functions.credits import death_screen
from utils.secondary_functions.health_output import Health_Output


def game_process_level_3(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()
    programIcon = pygame.image.load('data/world_design/characters/gold_carrot_ok.png')
    pygame.display.set_icon(programIcon)

    map_filename_1 = 'levels/level3_1.txt'
    map_filename_2 = 'levels/level3_2.txt'
    map_filename_3 = 'levels/level3_3.txt'
    map_filename_4 = 'levels/level3_4.txt'
    map_filename_5 = 'levels/level3_5.txt'

    current_map_filename = map_filename_3

    change_player_pos_on_map(current_map_filename, (4, 3))
    set_tile(map_filename_3, '.', (4, 3))

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
    heals_group = pygame.sprite.Group()

    success = True

    class Tile(pygame.sprite.Sprite):
        tile_images = {'empty': ['', (0, 0)],
                       'Bush-4.png': [load_image('world_design/Bushes/Bush-4.png', scale_size=(74, 74)), (13, 26)],
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
                       'Sculture-2.png': [load_image('world_design/Sculptures/Sculture-2.png'), (0, 0)],
                       'Sculpture-1.png': [load_image('world_design/Sculptures/Sculpture-1.png'), (0, 0)],
                       'box.png': [load_image('world_design/Stones/box.png'), (0, 0)],
                       'light_earth.png': [load_image('world_design/Ground/light_earth.png'), (0, 0)],
                       'Tree-1-4.png': [load_image('world_design/Trees/Tree-1/Tree-1-4.png'), (0, 0)],
                       'portal.png': [load_image('world_design/points/portal.png'), (0, 0)],
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
            elif len(args) == 1 and args[0].startswith('remove '):
                obj = args[0].split()[1]
                if obj in self.tile_type:
                    tiles_group.remove(self)

    class Heal(pygame.sprite.Sprite):
        image = load_image('world_design/points/heal.png')

        def __init__(self, pos):
            super(Heal, self).__init__(heals_group)
            self.image = Heal.image
            self.pos = pos
            self.rect = self.image.get_rect().move(
                tile_width * pos[0], tile_height * pos[1])

        def update(self):
            if player.pos == self.pos:
                player.heal(1)
                heals_dict[current_map_filename].remove(self)
                heals_group.remove(self)

    heals_dict = {map_filename_1: [Heal((1, 2))],
                  map_filename_2: [Heal((2, 7))],
                  map_filename_3: [Heal((2, 0)), Heal((7, 2)), Heal((3, 7)), Heal((9, 7))],
                  map_filename_4: [Heal((0, 7))],
                  map_filename_5: []}

    class Tip(pygame.sprite.Sprite):
        def __init__(self, text):
            super().__init__(tip_grooup)
            self.text = text
            self.font = pygame.font.Font(None, 35)
            self.output_text = self.font.render(self.text, True, (255, 255, 255))
            self.place = self.output_text.get_rect(center=(500, 900))

        def print_tip(self):
            self.clear()
            self.output_text = self.font.render(self.text, True, (255, 255, 255))
            self.place = self.output_text.get_rect(center=(500, 900))
            screen.blit(self.output_text, self.place)

        def clear(self):
            self.output_text.fill((0, 0, 0))
            screen.blit(self.output_text, self.place)

    class Bell(pygame.sprite.Sprite):
        bell_image = load_image('world_design/points/bell.png')
        clear_image = load_image('world_design/characters/clear.png')

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

        def hide(self):
            self.image = Bell.clear_image

        def show(self):
            self.image = Bell.bell_image

    def get_bell(bell_num):
        result = [elem for elem in bells_group if elem.bell_num == bell_num]
        if result:
            return result[0]
        return None

    class Player(pygame.sprite.Sprite):
        player_ok_image = load_image('world_design/characters/gold_carrot_ok.png')
        player_with_salt_image = load_image('world_design/characters/gold_carrot_with_salt.png')
        player_with_flower_image = load_image('world_design/characters/gold_carrot_with_flower.png')
        player_with_gun_image = load_image('world_design/characters/gold_carrot_with_gun.png')

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

        def flower_image(self):
            self.image = Player.player_with_flower_image

        def salt_image(self):
            self.image = Player.player_with_salt_image

        def ok_image(self):
            self.image = Player.player_ok_image

        def gun_image(self):
            self.image = Player.player_with_gun_image

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
            current_map_filename = end_map
            change_player_pos_on_map(current_map_filename, end_pos)
            level_map, player_pos = load_level(current_map_filename)
            tiles_group.empty()
            doors_group.empty()
            bells_group.empty()
            heals_group.empty()
            generate_level(level_map)
            heals_group.add(*heals_dict[current_map_filename])
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

    possible_to_move_objects = {'.', 'red_point.png', 'blue_door_left.png-3_4', 'dirty_row.png',
                                'blue_door_right.png-3_2', 'blue_door_down.png-3_3', 'blue_door_up.png-3_1',
                                'blue_door_down.png-1_1', 'blue_door_right.png-2_1', 'blue_door_left.png-4_1',
                                'blue_door_up.png-5_1', 'portal.png'}

    def check_story_status():
        nonlocal story_status, running
        if story_status == 'beet1' and player.pos == (9, 6) and current_map_filename == map_filename_4:
            bell = get_bell('4_2')
            bell.hide()
            Tile('beet.png', 9, 7)
            if not dialog_with_beet1.check_start_dialog():
                tiles_group.update('remove beet')
                bell.show()
                story_status = 'watermelon1'
            return 'beet1'
        elif story_status == 'watermelon1' and player.pos == (1, 0) and current_map_filename == map_filename_1:
            bell = get_bell('1_1')
            bell.hide()
            Tile('watermelon.png', 0, 0)
            if not dialog_with_melon.check_start_dialog():
                tiles_group.update('remove watermelon')
                bell.show()
                story_status = 'pumpkin1'
            return 'watermelon1'
        elif story_status == 'pumpkin1' and player.pos == (0, 1) and current_map_filename == map_filename_2:
            bell = get_bell('2_1')
            bell.hide()
            Tile('pumpkin.png', 0, 0)
            if not dialog_with_pumpkin1.check_start_dialog():
                tiles_group.update('remove pumpkin')
                bell.show()
                possible_to_move_objects.add('Flower-3.png')
                story_status = 'flower 1'
            return 'pumpkin1'
        elif story_status == 'flower 1' and player.pos == (4, 4) and current_map_filename == map_filename_5:
            flower = [elem for elem in tiles_group if elem.tile_type == 'Flower-3.png'][0]
            tiles_group.remove(flower)
            player.flower_image()
            story_status = 'pumpkin2'
        elif story_status == 'pumpkin2' and player.pos == (0, 1) and current_map_filename == map_filename_2:
            bell = get_bell('2_1')
            bell.hide()
            Tile('pumpkin.png', 0, 0)
            if not dialog_with_pumpkin2.check_start_dialog():
                tiles_group.update('remove pumpkin')
                bell.show()
                player.salt_image()
                story_status = 'beet2'
            return 'pumpkin2'
        elif story_status == 'beet2' and player.pos == (9, 6) and current_map_filename == map_filename_4:
            bell = get_bell('4_2')
            bell.hide()
            Tile('beet.png', 9, 7)
            if not dialog_with_beet2.check_start_dialog():
                tiles_group.update('remove beet')
                bell.show()
                player.ok_image()
                story_status = 'apple1'
            return 'beet2'
        elif story_status == 'apple1' and player.pos == (8, 0) and current_map_filename == map_filename_1:
            bell = get_bell('1_2')
            bell.hide()
            Tile('apple.png', 9, 0)
            if not dialog_with_apple2.check_start_dialog():
                tiles_group.update('remove apple')
                bell.show()
                player.gun_image()
                # портал в центре третьей карты
                set_tile(map_filename_3, 'portal.png', (4, 3))
                story_status = 'create portal'
            return 'apple1'
        elif story_status == 'create portal' and current_map_filename == map_filename_3:
            story_status = 'go to portal'
        elif story_status == 'go to portal' and player.pos == (4, 3) and current_map_filename == map_filename_3:
            change_player_pos_on_map(current_map_filename, (4, 3))
            running = False
        else:
            return False

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

        heals_group.update()
        # грядки
        if level_map[player.pos[1]][player.pos[0]] == 'dirty_row.png':
            player.damage(1)

    dialog_with_parrot = Dialog(dialogs_group, 'data/dialogs/dialog6.txt', (4, 3))
    dialog1_started = False
    dialog_with_beet1 = Dialog(dialogs_group, 'data/dialogs/dialog7.txt', (9, 6))
    dialog2_started = False
    dialog_with_melon = Dialog(dialogs_group, 'data/dialogs/dialog8.txt', (1, 0))
    dialog3_started = False
    dialog_with_pumpkin1 = Dialog(dialogs_group, 'data/dialogs/dialog9.txt', (0, 1))
    dialog4_started = False
    dialog_with_pumpkin2 = Dialog(dialogs_group, 'data/dialogs/dialog10.txt', (0, 1))
    dialog5_started = False
    dialog_with_beet2 = Dialog(dialogs_group, 'data/dialogs/dialog11.txt', (9, 6))
    dialog6_started = False
    dialog_with_apple2 = Dialog(dialogs_group, 'data/dialogs/dialog12.txt', (8, 0))
    dialog7_started = False

    story_status = 'beet1'
    dialog_status = False

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    screen.fill((0, 0, 0))
    save_level(3)

    heals_group.empty()
    heals_group.add(*heals_dict[current_map_filename])
    heals_group.add(*heals_dict[current_map_filename])

    health_string = Health_Output(screen, (500, 825), player.hp)

    damage_sound = pygame.mixer.Sound('data/music/damage_sound_full.mp3')
    damage_sound.set_volume(0.5)

    running = True
    pygame.mixer.music.load('data/music/main_sound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.04)
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
                # штуки с диалогами в функцию
                if dialog1_started and dialog_with_parrot.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_3:
                    if dialog_with_parrot.check_start_dialog():
                        dialog_with_parrot.next_string(screen)
                    if not dialog_with_parrot.check_start_dialog():
                        dialog_status = False

                if dialog2_started and dialog_with_beet1.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_4 and not dialog6_started:
                    if dialog_with_beet1.check_start_dialog():
                        dialog_with_beet1.next_string(screen)
                    if not dialog_with_beet1.check_start_dialog():
                        dialog_status = False

                if dialog3_started and dialog_with_melon.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_1:
                    if dialog_with_melon.check_start_dialog():
                        dialog_with_melon.next_string(screen)
                    if not dialog_with_melon.check_start_dialog():
                        dialog_status = False

                if dialog4_started and dialog_with_pumpkin1.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_2:
                    if dialog_with_pumpkin1.check_start_dialog():
                        dialog_with_pumpkin1.next_string(screen)
                    if not dialog_with_pumpkin1.check_start_dialog():
                        dialog_status = False

                if dialog5_started and dialog_with_pumpkin2.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_2:
                    if dialog_with_pumpkin2.check_start_dialog():
                        dialog_with_pumpkin2.next_string(screen)
                    if not dialog_with_pumpkin2.check_start_dialog():
                        dialog_status = False

                if dialog6_started and dialog_with_beet2.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_4:
                    if dialog_with_beet2.check_start_dialog():
                        dialog_with_beet2.next_string(screen)
                    if not dialog_with_beet2.check_start_dialog():
                        dialog_status = False

                if dialog7_started and dialog_with_apple2.check_position(player.pos, screen) and\
                        current_map_filename == map_filename_1:
                    if dialog_with_apple2.check_start_dialog():
                        dialog_with_apple2.next_string(screen)
                    if not dialog_with_apple2.check_start_dialog():
                        dialog_status = False

        if not success:
            return False

        if player.pos == (4, 3) and not dialog1_started and current_map_filename == map_filename_3:
            dialog_with_parrot.next_string(screen)
            dialog1_started = True

        status = check_story_status()

        if status == 'beet1' and not dialog2_started:
            dialog_with_beet1.next_string(screen)
            dialog2_started = True
            dialog_status = True

        elif status == 'watermelon1' and not dialog3_started:
            dialog_with_melon.next_string(screen)
            dialog3_started = True
            dialog_status = True

        elif status == 'pumpkin1' and not dialog4_started:
            dialog_with_pumpkin1.next_string(screen)
            dialog4_started = True
            dialog_status = True

        elif status == 'pumpkin2' and not dialog5_started:
            dialog_with_pumpkin2.next_string(screen)
            dialog5_started = True
            dialog_status = True

        elif status == 'beet2' and not dialog6_started:
            dialog_with_beet2.next_string(screen)
            dialog6_started = True
            dialog_status = True

        elif status == 'apple1' and not dialog7_started:
            dialog_with_apple2.next_string(screen)
            dialog7_started = True
            dialog_status = True

        check_doors()

        tiles_group.draw(screen)
        doors_group.draw(screen)
        bells_group.draw(screen)
        player_group.draw(screen)
        heals_group.draw(screen)
        tiles_group.update()
        if not dialog_status:
            bells_group.update()
        draw_lines(screen)
        health_string.update_hp(screen, player.hp)

        pygame.display.flip()
        clock.tick(FPS)

    set_hp(player.hp)
    return True


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 900)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_3(screen)
