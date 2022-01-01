import pygame
from credits import credits, get_credits_text


def init_game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 800))
    final_credits_text = get_credits_text('credits_texts/final_credits.txt')
    opening_credits_text = get_credits_text('credits_texts/opening_credits.txt')
    fps = 60
    running = True
    screen.fill((0, 0, 0))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for elem in opening_credits_text:
                        credits(screen, elem)
                        pygame.display.flip()
                        pygame.time.wait(3000) #Таймер, чтобы можно было прочитать текст

                if event.button == 3:

                    for elem in final_credits_text:
                        credits(screen, elem)
                        pygame.display.flip()
                        pygame.time.wait(3000) #Таймер, чтобы можно было прочитать текст

        pygame.display.flip()
        clock.tick(fps)


init_game()