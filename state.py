import pygame
import configs


class GameState:
    points = 0
    running = False
    dino_rect: pygame.rect.Rect = None
    floor_rect: pygame.rect.Rect = None

    def __init__(self):
        self.level = 1
        self.all_sprites_group = pygame.sprite.Group()
        self.trees_sprites_group = pygame.sprite.Group()

    def add_point(self):
        self.points += 1

    def add_dino_rect(self, position: pygame.rect.Rect):
        self.dino_rect = position

    def add_floor_rect(self, position: pygame.rect.Rect):
        self.floor_rect = position

    def start_game(self):
        self.running = True

    def stop_game(self):
        self.running = False

    def get_tick(self):
        self.level = int(self.points / configs.NEW_LEVEL_POINT) + 1
        return configs.CLOCK_TICK + (
                (self.points / configs.NEW_LEVEL_POINT) * configs.CLOCK_INCREASING_BY_LEVEL)
