import os
import random
import sys
import pygame

FPS = 60

pygame.init()
size = width, height = (1000, 900)
tile_width, tile_height = 100, 100
pygame.display.set_caption("Перемещение героя")
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("white"))
clock = pygame.time.Clock()


def load_image(name, color_key=None, scale_size=(tile_width, tile_height)):
    scale_size: tuple
    fullname = os.path.join('data/', name)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    if scale_size:
        image = pygame.transform.scale(image, scale_size)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile('empty', x, y)
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'c':
                Tile('chest', x, y)
            elif level[y][x] == 's':
                Tile('sculpture-1', x, y)
            elif level[y][x] == 'p':
                Tile("chest", x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


tile_images = {
    'wall': {'image': load_image('world_design/Bushes/Bush-1.png'),
             'indent': (0, 0)},  # отступ от края ячейки
    'chest': {'image': load_image('world_design/Bench and chest/Chest.png', scale_size=(75,) * 2),
              'indent': (12, 25)},
    'empty': {'indent': (0, 0)},
    'sculpture-1': {'image': load_image('world_design/Sculptures/Sculpture-1.png', scale_size=(74, 100)),
                    'indent': (13, 2)}
}
player_image = load_image('world_design/gold_carrot.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group)
        if tile_type == "empty":
            self.image = load_image(f"world_design/Ground/Dark-grass-{random.randint(1, 4)}.png")
        else:
            self.image = tile_images[tile_type]['image']

        indent_x, indent_y = tile_images[tile_type]['indent']
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


def change_player_pos_on_map(filename, pos_before, pos):
    with open(filename, "r", encoding="utf-8") as map_file:
        data = map_file.readlines()

    data = [list(elem.strip()) for elem in data]
    data[pos_before[1]][pos_before[0]] = "."
    data[pos[1]][pos[0]] = "@"

    data = ["".join(elem) for elem in data]
    with open(filename, "w", encoding="utf-8") as map_file:
        map_file.write("\n".join(data))


def move(player, movement):
    global level_map
    level_map = load_level('map.txt')

    x, y = pos_before = player.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            player.move(x, y - 1)
    if movement == "down":
        if y < level_y and level_map[y + 1][x] == ".":
            player.move(x, y + 1)
    if movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            player.move(x - 1, y)
    if movement == "right":
        if x < level_x and level_map[y][x + 1] == ".":
            player.move(x + 1, y)

    change_player_pos_on_map("data/map.txt", pos_before, player.pos)
    level_map = load_level('map.txt')


def draw_lines(screen):
    color = (48, 77, 46)
    [pygame.draw.line(screen, color, (x, 0), (x, 800), 1) for x in range(0, width, tile_width)]
    [pygame.draw.line(screen, color, (0, y), (width, y), 1) for y in range(0, 800, tile_height)]


level_map = load_level('map.txt')
player, level_x, level_y = generate_level(level_map)


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
