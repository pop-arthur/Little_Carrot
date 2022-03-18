import pygame


def get_text(file_name):
    with open(file_name, 'r') as text_file:
        text = list(map(lambda x: x.strip(), text_file.readlines()))
        text.append('')
    return text


class Dialog(pygame.sprite.Sprite):
    def __init__(self, group, file_name, position):
        super().__init__(group)
        self.text = get_text(file_name)
        self.font = pygame.font.Font(None, 35)
        self.cell_text = 0
        self.flag = True
        self.pos = position

    def next_string(self, screen):
        self.clear(screen)
        self.output_text = self.font.render(self.text[self.cell_text], True, (255, 255, 255))
        self.place = self.output_text.get_rect(center=(500, 900))
        screen.blit(self.output_text, self.place)
        self.cell_text += 1
        self.output_text.fill((0, 0, 0))

    def clear(self, screen):
        if self.cell_text > 0:
            self.output_text.fill((0, 0, 0))
            screen.blit(self.output_text, self.place)

    def check_position(self, player_pos, screen):
        if player_pos != self.pos:
            self.clear(screen)
            return False
        return True

    def check_start_dialog(self):
        if self.cell_text + 1 > len(self.text):
            self.flag = False
        return self.flag
