from game_init_functions import *

counter = 0
for i in range(1, 6):
    print(i, end='\t')
    map_filename = f'levels/level3_{i}.txt'
    level_map, player_pos = load_level(map_filename)
    for y in range(8):
        for x in range(10):
            if level_map[y][x] == 'heal.png':
                set_tile(map_filename, '.', (x, y))
                print(x, y, end=',\t')
    print()
