from game_init_functions import *
from db_functions import *
import pygame
import random


def draw_lines(screen):
    color = (48, 77, 46)
    [pygame.draw.line(screen, color, (x, 0), (x, 1000), 1) for x in range(0, 1000, 100)]
    [pygame.draw.line(screen, color, (0, y), (1000, y), 1) for y in range(0, 1000, 100)]
    # pygame.draw.line(screen, color, (0, 850), (1000, 850), 1)


def capture(display, name, pos, size):  # (pygame Surface, String, tuple, tuple)
    image = pygame.Surface(size)  # Create image surface
    image.blit(display, (0,0), (pos, size))  # Blit portion of the display to the image
    pygame.image.save(image, name)  # Save the image to the disk


def game_process_level_4(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()

    map_filename_1 = 'levels/picture_map.txt'
    current_map_filename = map_filename_1

    max_x = 10
    max_y = 9

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    dialogs_group = pygame.sprite.Group()
    tip_grooup = pygame.sprite.Group()
    scarecrows_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    portal = pygame.sprite.Sprite()

    class Tile(pygame.sprite.Sprite):
        tile_images = {'empty': ['', (0, 0)],
                       'Bush-4.png': [load_image('world_design/Bushes/Bush-4.png', scale_size=(74, 74)), (13, 13)],
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
                       'egg.png': [load_image('world_design/characters/egg.png'), (0, 0)],
                       'potato.png': [load_image('world_design/characters/potato.png'), (0, 0)],
                       'parrot.png': [load_image('world_design/characters/parrot.png'), (0, 0)],
                       'Sculture-2.png': [load_image('world_design/Sculptures/Sculture-2.png'), (0, 0)],
                       'Sculpture-1.png': [load_image('world_design/Sculptures/Sculpture-1.png'), (0, 0)],
                       'box.png': [load_image('world_design/Stones/box.png'), (0, 0)],
                       'light_earth.png': [load_image('world_design/Ground/light_earth.png'), (0, 0)],
                       'Tree-1-4.png': [load_image('world_design/Trees/Tree-1/Tree-1-4.png'), (0, 0)],
                       'portal.png': [load_image('world_design/points/portal.png'), (0, 0)],
                       'heal.png': [load_image('world_design/points/heal.png'), (0, 0)],
                       'Flower-3.png': [load_image('world_design/Flowers/Flower-3.png'), (0, 0)]}
        clear_image = load_image('world_design/characters/clear.png')

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

        def hide(self):
            self.image = Tile.clear_image

        def show(self):
            image, indent = Tile.tile_images[self.tile_type]
            self.image = image

    class Scarecrow(pygame.sprite.Sprite):
        image = load_image('world_design/characters/scarecrow.png', scale_size=(90, 90))

        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, scarecrows_group)
            self.pos = (pos_x, pos_y)
            self.image = Scarecrow.image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 5, tile_height * pos_y + 5)
            self.hp = 3
            self.group = pygame.sprite.Group()
            self.group.add(self)

        def update(self):
            if pygame.sprite.groupcollide(bullets_group, self.group, True, False):
                self.hp -= 1
                if self.hp == 0:
                    self.kill()

    class Player(pygame.sprite.Sprite):
        player_with_gun_image = load_image('world_design/characters/gold_carrot_ok.png', scale_size=(200, 200))

        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = Player.player_with_gun_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 10, tile_height * pos_y)
            self.pos = (pos_x, pos_y)
            self.centerx = 50
            self.bottom = 90
            self.speedx = 0
            self.hp = get_current_hp()

        def move(self, x, y):
            self.pos = (x, y)
            self.rect = self.image.get_rect().move(
                tile_width * x + 5, tile_height * y)

        def check_parrot(self):
            if self.pos == (4, 2):
                return True
            return False

        def heal(self, count_of_heal):
            self.hp += count_of_heal

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets_group.add(bullet)

    def generate_level(level):
        nonlocal portal
        for y in range(len(level)):
            for x in range(len(level[y])):
                Tile('empty', x, y)
                if level[y][x] == '.':
                    pass
                elif level[y][x] == 'scarecrow.png':
                    Scarecrow(x, y)
                elif level[y][x] == 'portal.png':
                    portal = Tile(level[y][x], x, y)
                    portal.hide()
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

    class Bullet(pygame.sprite.Sprite):
        bullet_image = load_image('world_design/characters/gold_carrot_with_gun.png', scale_size=(20, 30))

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = Bullet.bullet_image
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            # убить, если он заходит за верхнюю часть экрана
            if self.rect.bottom < 0:
                self.kill()

    level_map, player_pos = load_level(current_map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    screen.fill((0, 0, 0))

    captured = False

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
                if event.key == pygame.K_SPACE:
                    player.shoot()

        tiles_group.draw(screen)
        scarecrows_group.draw(screen)
        bullets_group.draw(screen)
        tiles_group.update()
        draw_lines(screen)
        all_sprites.update()
        if pygame.sprite.groupcollide(bullets_group, scarecrows_group, False, False):
            scarecrows_group.update()
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        if not captured:
            capture(screen, "data/credits_texts/final_image.png", (0, 0), (1000, 850))
            captured = True

    set_hp(player.hp)
    return True


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 950)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_4(screen)
