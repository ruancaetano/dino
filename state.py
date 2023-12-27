import pygame
import configs


class GameState:
    points = {}
    max_point = 0
    running = False
    dino_rects_map = {}
    floor_rect: pygame.rect.Rect = None

    def __init__(self):
        self.level = 1
        self.all_sprites_group = pygame.sprite.Group()
        self.trees_sprites_group = pygame.sprite.Group()

    def add_point(self, dino_id: int):
        self.points[dino_id] += 1
        if self.points[dino_id] > self.max_point:
            self.max_point = self.points[dino_id]

    def add_floor_rect(self, position: pygame.rect.Rect):
        self.floor_rect = position

    def start_game(self):
        self.running = True

    def stop_game(self):
        self.running = False

    def get_tick(self):
        self.level = int(self.max_point / configs.NEW_LEVEL_POINT) + 1
        return configs.CLOCK_TICK + (
                (self.max_point / configs.NEW_LEVEL_POINT) * configs.CLOCK_INCREASING_BY_LEVEL)
