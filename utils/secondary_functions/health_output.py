import pygame

class Health_Output():
    def __init__(self, screen, place, count, string='HP', size=35):
        self.string = string
        self.font = pygame.font.Font(None, size)
        self.output_text = self.font.render(f"{self.string}: {str(count)}", True, (255, 255, 255))
        self.place = self.output_text.get_rect(center=(place))
        screen.blit(self.output_text, self.place)

    def update_hp(self, screen, count):
        self.output_text.fill((0, 0, 0))
        screen.blit(self.output_text, self.place)
        self.output_text = self.font.render(f"{self.string}: {str(count)}", True, (255, 255, 255))
        screen.blit(self.output_text, self.place)