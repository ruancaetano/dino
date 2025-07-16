import pygame
import random
from game import configs

WIDTH = 80
HEIGHT = 42


class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("sprites/cloud-1.png"), (WIDTH, HEIGHT))

        self.rect = self.surf.get_rect(
            center=(
                configs.SCREEN_WIDTH,
                random.randint(50, 200)  # Cloud height range
            )
        )

    def update(self, game_speed):
        # Parallax effect: clouds move slower than obstacles
        cloud_speed = game_speed * configs.CLOUD_PARALLAX_RATIO
        self.rect.move_ip(-cloud_speed, 0)

        if self.rect.x < -WIDTH/2:
            self.kill()
