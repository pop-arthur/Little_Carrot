import random
from game_init_functions import *
from db_functions import *
from dialogs import Dialog


def game_process_level_1(screen):
    FPS = 60
    tile_width, tile_height = 100, 100
    clock = pygame.time.Clock()

    max_x = 9
    max_y = 7

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

        def check_parrot(self):
            if self.pos == (4, 2):
                return True
            return False

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
    dialogs_group = pygame.sprite.Group()
    rect_group = pygame.sprite.Group()

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
                   'apple.png': [load_image('world_design/characters/apple.png', color_key=-1), (0, 0)],
                   'Stone-1.png': [load_image('world_design/Stones/Stone-1.png', scale_size=(74, 90)), (13, 10)]}
    player_image = load_image('world_design/characters/gold_carrot_ok.png')

    class RedRect(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, player_group)
            self.image = load_image('world_design/points/red_point.png', scale_size=(90, 90))
            self.rect = self.image.get_rect().move(pos_x, pos_y)

    def generate_level(level):
        new_player, x, y = None, None, None
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
        nonlocal level_map
        level_map = load_level(map_filename)[0]

        x, y = player.pos
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

        level_map = load_level(map_filename)

    level_map, player_pos = load_level(map_filename)
    player = Player(*player_pos)
    generate_level(level_map)

    for i in range(256):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((i,) * 3)
        pygame.display.flip()
        clock.tick(FPS)

    def create_right_pos():
        pos_x, pos_y = random.choice(list_of_x), random.choice(list_of_y)
        while (pos_x in [206, 306, 406, 506, 606, 706] and pos_y == 106) or (pos_x == 306 and pos_y == 606) or \
                (pos_x == 506 and pos_y == 206) or (pos_x == 606 and pos_y == 506):
            pos_x, pos_y = random.choice(list_of_x), random.choice(list_of_y)
        return pos_x, pos_y

    list_of_x = [5, 106, 206, 306, 406, 506, 606, 706, 806, 906]
    list_of_y = [5, 106, 206, 306, 406, 506, 606, 706]
    counter_1, counter_2 = 0, 0
    sprites_collide = False
    start_apple = False
    start_apple_dialog = False
    apple_pos = (1, 4)

    dialog_with_parrot = Dialog(dialogs_group, 'data/dialogs/dialog1.txt', (4, 2))
    dialog_with_apple = Dialog(dialogs_group, 'data/dialogs/dialog2.txt', (2, 4))
    dialog1_started = True
    dialog2_started = False
    start_points = False
    screen.fill((0, 0, 0))
    # save_level(1)

    running = True
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_tile(map_filename, '.', apple_pos)
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
                if player.check_parrot() and dialog_with_parrot.check_start_dialog():
                    dialog_with_parrot.next_string(screen)

                if dialog_with_apple.check_position(player.pos, screen) and dialog_with_apple.check_start_dialog() and\
                        not dialog_with_parrot.check_start_dialog() and start_apple_dialog:
                    dialog_with_apple.next_string(screen)

        if dialog1_started:
            dialog_with_parrot.next_string(screen)
            dialog1_started = False
        if not dialog_with_parrot.check_start_dialog() and start_points is False:
            pos = create_right_pos()
            red_rect = RedRect(pos[0], pos[1])
            rect_group.add(red_rect)
            start_points = True

        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        draw_lines(screen)
        grass = load_image('world_design/Ground/Dark-grass-1.png')
        if sprites_collide is True and counter_1 <= 9:
            rect_group.clear(screen, grass)
            pygame.display.update()
            counter_1 += 1
        elif sprites_collide and counter_1 >= 10:
            start_apple = True
            dialog2_started = True

        sprites_collide = False

        if pygame.sprite.spritecollide(player, rect_group, True):
            sprites_collide = True
        elif counter_1 > counter_2:
            pos = create_right_pos()
            rect_group.add(RedRect(pos[0], pos[1]))
            rect_group.draw(screen)
            counter_2 += 1

        if start_apple:
            start_apple_dialog = True
            Tile('apple.png', *apple_pos)
            set_tile(map_filename, 'apple.png', apple_pos)
            #RedRect(200, 400)
            start_apple = False

        if dialog_with_apple.check_position(player.pos, screen) and dialog2_started:
            dialog2_started = False
            if dialog_with_apple.check_start_dialog():
                dialog_with_apple.next_string(screen)

        if not dialog_with_apple.check_start_dialog():
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    set_tile(map_filename, '.', apple_pos)

    class Star(pygame.sprite.Sprite):
        # сгенерируем частицы разного размера
        def __init__(self, pos, dx, dy, n_frames=1):
            self.fire = [load_image("world_design/points/star.png")]
            for scale in (5, 10, 20):
                self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
            super().__init__(all_sprites)
            self.image = random.choice(self.fire)
            self.rect = self.image.get_rect()

            # у каждой частицы своя скорость — это вектор
            self.velocity = [dx, dy]
            # и свои координаты
            self.rect.x, self.rect.y = pos

            # гравитация будет одинаковой (значение константы)
            self.gravity = random.randint(-2, 2)

            self.n_frames = n_frames

        def update(self):
            # применяем гравитационный эффект:
            # движение с ускорением под действием гравитации
            self.velocity[1] += self.gravity // self.n_frames
            # перемещаем частицу
            self.rect.x += self.velocity[0] // self.n_frames
            self.rect.y += self.velocity[1] // self.n_frames
            # убиваем, если частица ушла за экран
            if not self.rect.colliderect(screen_rect):
                self.kill()

    def create_particles(position, n_frames=1):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        for _ in range(particle_count):
            Star(position, random.randint(-5, 5), random.randint(-5, 5), n_frames)

    screen_rect = (0, 0, 1000, 900)
    all_sprites = pygame.sprite.Group()
    timer = 0
    frequency = 5
    for i in range(300):
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if timer % frequency == 0:
            timer = 0
            create_particles((random.randint(25, 975), random.randint(25, 875)))
            create_particles((random.randint(25, 975), random.randint(25, 875)))
            create_particles((random.randint(25, 975), random.randint(25, 875)))

        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 900)
    pygame.display.set_caption("Little Carrot")
    screen = pygame.display.set_mode(size)
    game_process_level_1(screen)
