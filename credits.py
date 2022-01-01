import pygame


def get_credits_text(file_name):
    with open(file_name, 'r') as credits_file:
        credits_text = list(map(lambda x: x.strip(), credits_file.readlines()))
    return credits_text


def credits(screen, text):  # В функцию приходит Surface, на котором будет изображен текст, и строчка текста
    credits_font = pygame.font.Font(None, 56)
    output_text = credits_font.render(text, True, (255, 255, 255))
    place = output_text.get_rect(center=(500, 350))  # Отцентровка текста

    screen.fill((0, 0, 0))  # Очищение Surface для написания текста
    screen.blit(output_text, place)
