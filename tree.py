import pygame

import configs
import floor
import state

WIDTH = 60
HEIGHT = 52.5
WALK_WIDTH = 10
HORIZONTAL_PADDING = 50

CENTER_Y_ON_FLOOR = configs.SCREEN_HEIGHT - floor.HEIGHT - HEIGHT / 2

SPRITE_NAME_PREFIX = "tree-"

sprites_images = {
    SPRITE_NAME_PREFIX + "1": pygame.transform.scale(pygame.image.load("sprites/tree-1.png"), (WIDTH, HEIGHT))
}


class Tree(pygame.sprite.Sprite):
    scored = False
    dino_rect = None
    game_state = None

    def __init__(self, dino_rect: pygame.rect.Rect, game_state: state.GameState):
        super(Tree, self).__init__()
        self.surf = sprites_images[SPRITE_NAME_PREFIX + "1"]
        self.rect = self.surf.get_rect(
            center=(
                configs.SCREEN_WIDTH - HORIZONTAL_PADDING,
                CENTER_Y_ON_FLOOR
            )
        )
        self.dino_rect = dino_rect
        self.game_state = game_state

    def update(self, pressed_keys):
        self.rect.move_ip(-WALK_WIDTH, 0)

        if self.rect.x < -WIDTH/2:
            self.kill()

        if self.rect.x < self.dino_rect.x and not self.scored:
            self.scored = True
            self.game_state.add_point()
