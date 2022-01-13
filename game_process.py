import pygame
from credits import show_start_credits, show_end_credits
from game_init_functions import terminate
from level1 import game_process_level_1
from level2 import game_process_level_2
from level3 import game_process_level_3
from level4 import game_process_level_4
from level5 import game_process_level_5
from db_functions import get_level, save_level


def init_game():
    save_level(3)
    level = get_level()

    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption("Little Carrot")

    if level == 0:
        show_start_credits(screen)
        save_level(1)
        level = get_level()

    if level == 1:
        game_process_level_1(screen)
        save_level(2)
        level = get_level()

    if level == 2:
        success = game_process_level_2(screen)
        while not success:
            success = game_process_level_2(screen)

        save_level(3)
        level = get_level()

    if level == 3:
        success = game_process_level_3(screen)
        while not success:
            success = game_process_level_3(screen)

        save_level(4)
        level = get_level()

    if level == 4:
        success = game_process_level_4(screen)
        while not success:
            success = game_process_level_4(success)

        save_level(5)
        level = get_level()

    if level == 5:
        success = game_process_level_5(screen)
        while not success:
            success = game_process_level_5(screen)

        save_level(6)
        level = get_level()

    if level == 6:
        show_end_credits(screen)

    save_level(0)

    terminate()


if __name__ == '__main__':
    init_game()

