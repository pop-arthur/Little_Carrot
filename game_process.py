import pygame
from credits import show_start_credits, show_end_credits


def init_game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 800))

    fps = 60
    running = True

    show_start_credits(screen)
    show_end_credits(screen)

    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     screen.fill("black")
    #
    #     pygame.display.flip()
    #     clock.tick(fps)
