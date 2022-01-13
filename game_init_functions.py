import os
import pygame
import sys


def load_image(name, color_key=None, scale_size=(100, 100)):
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
        pass

    if scale_size:
        image = pygame.transform.scale(image, scale_size)
    return image


def change_player_pos_on_map(filename, pos):
    filename = "data/" + filename
    with open(filename, "r", encoding="utf-8") as map_file:
        data = map_file.readlines()[:-1] + [' '.join(map(str, pos))]

    with open(filename, "w", encoding="utf-8") as map_file:
        map_file.write("".join(data))


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        data = [line.strip() for line in mapFile]

    level_map, player_pos = data[:-1], list(map(int, data[-1].split()))

    level_map = [elem.split() for elem in level_map]
    return level_map, player_pos


def set_tile(filename, tile_type, pos):
    filename = "data/" + filename
    with open(filename, "r", encoding="utf-8") as map_file:
        data = map_file.readlines()

    data = list(map(str.split, data))
    data[pos[1]][pos[0]] = tile_type
    data = ['\t'.join(elem) for elem in data[:-1]] + [' '.join(data[-1])]
    data = '\n'.join(data)
    with open(filename, "w", encoding="utf-8") as map_file:
        map_file.write(data)


def draw_lines(screen):
    color = (48, 77, 46)
    [pygame.draw.line(screen, color, (x, 0), (x, 800), 1) for x in range(0, 1000, 100)]
    [pygame.draw.line(screen, color, (0, y), (1000, y), 1) for y in range(0, 800, 100)]
    pygame.draw.line(screen, color, (0, 850), (1000, 850), 1)

def terminate():
    pygame.quit()
    sys.exit()
