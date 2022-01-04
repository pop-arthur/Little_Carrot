import pygame
import random
from game_init_functions import load_image


class Egg(pygame.sprite.Sprite):
    #egg_image = load_image('world_design/characters/egg.png')
    def __init__(self, all_sprites, group):
        super().__init__(all_sprites, group)
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(600, 500, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self, screen):
        self.rect = self.rect.move(self.vx, self.vy)


