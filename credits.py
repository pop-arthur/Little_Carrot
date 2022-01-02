import pygame


def get_credits_text(file_name):
    with open(file_name, 'r') as credits_file:
        credits_text = list(map(lambda x: x.strip(), credits_file.readlines()))
    return credits_text


class Credits(pygame.sprite.Sprite):
    def __init__(self, group, file_name, timer):
        super().__init__(group)
        self.credit_text = get_credits_text(file_name)
        self.credits_font = pygame.font.Font(None, 56)
        self.cell_text = 0
        self.timer = timer
        self.counter = timer // 2

    def update(self, screen):
        self.counter += 1
        if self.counter == self.timer:  # Таймер
            self.output_text = self.credits_font.render(self.credit_text[self.cell_text], True, (255, 255, 255))
            self.place = self.output_text.get_rect(center=(500, 350))
            screen.fill((0, 0, 0))
            screen.blit(self.output_text, self.place)
            self.counter = 0
            self.cell_text += 1

    def check(self):  # Если вывелся весь файл, то флаг меняется на False
        if self.cell_text + 1 > len(self.credit_text):
            self.flag = False
        return self.flag

    def set_flag(self, flag):  # Изменение флага вручную
        self.flag = flag


def show_start_credits(screen):
    clock = pygame.time.Clock()
    # Создание групп для работы с титрами
    opening_credits_group = pygame.sprite.Group()
    final_credits_group = pygame.sprite.Group()

    opening_credits = Credits(opening_credits_group, 'data/credits_texts/opening_credits.txt', 120)
    opening_credits.set_flag(True)

    fps = 60
    running = True
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if opening_credits.check():  # Вывод начальной заставки
            opening_credits_group.update(screen)

        if not opening_credits.check():
            running = False

        pygame.display.flip()
        clock.tick(fps)


def show_end_credits(screen):
    clock = pygame.time.Clock()
    # Создание групп для работы с титрами
    opening_credits_group = pygame.sprite.Group()
    final_credits_group = pygame.sprite.Group()

    final_credits = Credits(final_credits_group, 'data/credits_texts/final_credits.txt', 120)
    final_credits.set_flag(True)

    fps = 60
    running = True
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if final_credits.check():  # Вывод конечных титр
            final_credits_group.update(screen)

        pygame.display.flip()
        clock.tick(fps)
