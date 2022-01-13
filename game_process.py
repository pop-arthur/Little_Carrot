import pygame
from credits import show_start_credits, show_end_credits
from level1 import game_process_level_1
from level2 import game_process_level_2
from level3 import game_process_level_3
from level4 import game_process_level_4
from level5 import game_process_level_5


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption("Little Carrot")

    show_start_credits(screen)

    game_process_level_1(screen)
    game_process_level_2(screen)
    game_process_level_3(screen)
    game_process_level_4(screen)
    game_process_level_5(screen)

    show_end_credits(screen)


if __name__ == '__main__':
    init_game()

