import pygame
from credits import Credits, get_credits_text


def init_game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 800))
    # Создание групп для работы с титрами
    opening_credits_group = pygame.sprite.Group()
    final_credits_group = pygame.sprite.Group()

    opening_credits = Credits(opening_credits_group, 'data/credits_texts/opening_credits.txt', 120)
    opening_credits.set_flag(True)
    final_credits = Credits(final_credits_group, 'data/credits_texts/final_credits.txt', 120)
    final_credits.set_flag(False)

    fps = 60
    running = True
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if opening_credits.check():  # Вывод начальной заставки
            opening_credits_group.update(screen)

        if final_credits.check():  # Вывод конечных титр
            final_credits_group.update(screen)

        if not opening_credits.check():  # Смена флага для финальных титр, после полного вывода начальных
            final_credits.set_flag(True)

        pygame.display.flip()
        clock.tick(fps)


init_game()
