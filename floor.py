import pygame

import configs

HEIGHT = 130


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super(Floor, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("sprites/floor.png"), (configs.SCREEN_WIDTH, HEIGHT))
        self.rect = self.surf.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT - (HEIGHT / 2)))
