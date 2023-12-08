import pygame
import random

import configs

WIDTH = 80
HEIGHT = 42
VELOCITY = 5


class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("sprites/cloud-1.png"), (WIDTH, HEIGHT))

        self.rect = self.surf.get_rect(
            center=(
                configs.SCREEN_WIDTH,
                random.randint(100, 250)
            )
        )

    def update(self, pressed_keys):
        self.rect.move_ip(-VELOCITY, 0)

        if self.rect.x < -WIDTH/2:
            self.kill()
