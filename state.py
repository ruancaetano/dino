import pygame
import configs


class GameState:
    running = False
    dino_rects_map = {}
    floor_rect: pygame.rect.Rect | None = None

    def __init__(self):
        self.points = {}
        self.max_point = 0
        self.all_sprites_group = pygame.sprite.Group()
        self.trees_sprites_group = pygame.sprite.Group()

    def add_point(self, dino_id: int):
        self.points[dino_id] += 1
        if self.points[dino_id] > self.max_point:
            self.max_point = self.points[dino_id]



    def start_game(self):
        self.running = True

    def stop_game(self):
        self.running = False

    def get_tick(self):
        # Constant frame rate, speed increases through obstacle movement
        return configs.CLOCK_TICK
