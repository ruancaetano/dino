import pygame

import configs
import floor
import state

WIDTH = 60
HEIGHT = 52.5
HORIZONTAL_PADDING = -50

CENTER_Y_ON_FLOOR = configs.SCREEN_HEIGHT - floor.HEIGHT - HEIGHT / 2

SPRITE_NAME_PREFIX = "tree-"

sprites_images = {
    SPRITE_NAME_PREFIX + "1": pygame.transform.scale(pygame.image.load("sprites/tree-1.png"), (WIDTH, HEIGHT))
}


class Tree(pygame.sprite.Sprite):
    game_state = None

    def __init__(self, game_state: state.GameState):
        super(Tree, self).__init__()
        self.surf = sprites_images[SPRITE_NAME_PREFIX + "1"]
        self.rect = self.surf.get_rect(
            center=(
                configs.SCREEN_WIDTH - HORIZONTAL_PADDING,
                CENTER_Y_ON_FLOOR
            )
        )
        self.game_state = game_state
        self.scored_dinos = set()  # Track which dinos have scored on this tree

    def update(self):
        # Continuous speed increase based on game time
        # Speed increases every 20 points instead of every point
        speed_level = max(0, (self.game_state.max_point - 1) // 20)  # Start level 1 at score 20
        current_speed = configs.BASE_GAME_SPEED + (speed_level * configs.SPEED_INCREASE_RATE)
        self.rect.move_ip(-current_speed, 0)

        if self.rect.x < -WIDTH/2:
            self.kill()

        # Use the current live dino mapping, not the snapshot
        for dino_id, dino_rect in self.game_state.dino_rects_map.items():
            if self.rect.x < dino_rect.x and dino_id not in self.scored_dinos:
                self.scored_dinos.add(dino_id)
                self.game_state.add_point(dino_id)
