from utils.game_functions.game_init_functions import *
from utils.db.db_functions import *
import pygame
import random
from utils.secondary_functions.credits import death_screen
from utils.secondary_functions.health_output import Health_Output


def game_process_level_5(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()
    timer = 0
    programIcon = pygame.image.load('data/world_design/characters/gold_carrot_ok.png')
    pygame.display.set_icon(programIcon)

    map_filename_1 = 'levels/level5.txt'
    current_map_filename = map_filename_1

    max_x = 10
    max_y = 8

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    dialogs_group = pygame.sprite.Group()
    tip_grooup = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    player_bullets_group = pygame.sprite.Group()
    boss_bullet_group = pygame.sprite.Group()

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

    class Boss(pygame.sprite.Sprite):
        image = load_image('world_design/characters/farmer.png', scale_size=(196, 400))

        def __init__(self):
            super(Boss, self).__init__(boss_group, all_sprites)
            self.image = Boss.image
            self.speed = 40
            self.pos = [2, 0]
            self.rect = self.image.get_rect().move(
                tile_width * self.pos[0] + 2, tile_height * self.pos[1] + 8)
            self.group = pygame.sprite.Group()
            self.group.add(self)
            self.hp = 100

        def damage(self):
            nonlocal running
            if pygame.sprite.groupcollide(player_bullets_group, boss_group, True, False):
                self.hp -= 1
                if self.hp == 0:
                    running = False
                    self.kill()

        def move(self):
            nonlocal timer
            if not timer % self.speed == 0:
                return
            timer = 0
            if self.speed > 7:
                self.speed -= 1
            moving = []
            if self.pos[0] != 0:
                moving.append(-1)
            if self.pos[0] != 8:
                moving.append(1)
            moving = random.choice(moving)
            self.pos[0] += moving
            self.rect = self.image.get_rect().move(
                tile_width * self.pos[0] + 2, tile_height * self.pos[1] + 8)

            digit = random.randint(0, 210)
            if digit % 5 == 0:
                Bullet(self.rect.centerx - 50, self.rect.bottom, 5, boss_bullet_group)
            elif digit % 5 == 1:
                Bullet(self.rect.centerx + 50, self.rect.bottom, 5, boss_bullet_group)

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
            self.centerx = 50
            self.bottom = 90
            self.speedx = 0
            self.hp = get_current_hp()

        def move(self, x, y):
            self.pos = (x, y)
            self.rect = self.image.get_rect().move(
                tile_width * x + 5, tile_height * y)

        def damage(self, count_of_damage):
            damage_sound.play()
            self.hp -= count_of_damage
            if self.hp <= 0:
                nonlocal success
                death_screen(screen)
                success = False

        def heal(self, count_of_heal):
            self.hp += count_of_heal

        def shoot(self):
            Bullet(self.rect.centerx, self.rect.top, -10, player_bullets_group)

    class Bullet(pygame.sprite.Sprite):
        bullet_image = load_image('world_design/characters/gold_carrot_with_gun.png', scale_size=(20, 30))

        def __init__(self, x, y, speedy, group):
            super(Bullet, self).__init__(group)
            self.image = Bullet.bullet_image
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = speedy

        def update(self):
            self.rect.y += self.speedy
            # убить, если он заходит за верхнюю часть экрана
            if self.rect.bottom < 0 or self.rect.bottom > 800:
                self.kill()

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
            if y > 4 and level_map[y - 1][x] in possible_to_move_objects:
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

    dialog_status = False

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    shoot_sound = pygame.mixer.Sound('data/music/piu_shoot_sound.mp3')
    shoot_sound.set_volume(0.5)
    damage_sound = pygame.mixer.Sound('data/music/damage_sound_cut.mp3')
    damage_sound.set_volume(0.5)

    save_level(5)
    screen.fill((0, 0, 0))

    boss = Boss()
    pleyer_health_string = Health_Output(screen, (500, 825), player.hp, string='YOU', size=30)
    boss_health_string = Health_Output(screen, (500, 900), boss.hp, string='BOSS')

    running = True
    pygame.mixer.music.load('data/music/boss_sound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

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
                if event.key == pygame.K_SPACE:
                    shoot_sound.play()
                    player.shoot()
                if event.key == pygame.K_h and event.mod & pygame.KMOD_LCTRL:
                    player.heal(1000)
            if event.type == pygame.MOUSEBUTTONUP:
                pass

        if not success:
            return False

        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        draw_lines(screen)
        boss_group.draw(screen)
        player_bullets_group.draw(screen)
        player_bullets_group.update()
        boss_bullet_group.draw(screen)
        boss_bullet_group.update()
        boss.move()
        pygame.draw.line(screen, (90, 0, 0), (0, 400), (1000, 400), 2)

        if pygame.sprite.groupcollide(player_bullets_group, boss_group, False, False):
            boss.damage()
        if pygame.sprite.groupcollide(boss_bullet_group, player_group, True, False):
            player.damage(1)

        pleyer_health_string.update_hp(screen, player.hp)
        boss_health_string.update_hp(screen, boss.hp)

        pygame.display.flip()
        clock.tick(FPS)
        timer += 1

    for i in range(255, -1, -1):
        screen.fill((i,) * 3)
        pygame.display.flip()
        clock.tick(FPS)

    set_hp(player.hp)
    return True


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 950)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_5(screen)
