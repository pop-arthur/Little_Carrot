import pygame
from utils.secondary_functions.credits import show_start_credits, show_end_credits
from utils.game_functions.game_init_functions import terminate
from utils.levels.level1 import game_process_level_1
from utils.levels.level2 import game_process_level_2
from utils.levels.level3 import game_process_level_3
from utils.levels.level4 import game_process_level_4
from utils.levels.level5 import game_process_level_5
from utils.db.db_functions import get_level, save_level, reset_player


def init_game():
    level = get_level()

    pygame.init()
    screen = pygame.display.set_mode((1000, 950))
    programIcon = pygame.image.load('data/world_design/characters/gold_carrot_ok.png')
    pygame.display.set_icon(programIcon)

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
        save_level(0)
        show_end_credits(screen)

    reset_player()
    terminate()


if __name__ == '__main__':
    init_game()

