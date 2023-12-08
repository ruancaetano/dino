import pygame

import configs
import floor

from pygame.locals import (
    K_UP,
    K_DOWN,
)

import state

WIDTH = 80
HEIGHT = 70
INITIAL_JUMP_VELOCITY = 15
HORIZONTAL_PADDING = 100
FALL_DAMPING_VALUE = 0.5
SPRITE_RUN_PREFIX = "run-"

sprites_images = {
    SPRITE_RUN_PREFIX + "1": pygame.transform.scale(pygame.image.load("./sprites/run-1.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "2": pygame.transform.scale(pygame.image.load("./sprites/run-2.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "3": pygame.transform.scale(pygame.image.load("./sprites/run-3.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "4": pygame.transform.scale(pygame.image.load("./sprites/run-4.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "5": pygame.transform.scale(pygame.image.load("./sprites/run-5.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "6": pygame.transform.scale(pygame.image.load("./sprites/run-6.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "7": pygame.transform.scale(pygame.image.load("./sprites/run-7.png"), (WIDTH, HEIGHT)),
    SPRITE_RUN_PREFIX + "8": pygame.transform.scale(pygame.image.load("./sprites/run-8.png"), (WIDTH, HEIGHT))
}


class Dino(pygame.sprite.Sprite):

    def __init__(self, game_state: state.GameState):
        super(Dino, self).__init__()
        self.using_accelerate_fall = False
        self.is_jumping = False
        self.is_downing = False
        self.jump_velocity = INITIAL_JUMP_VELOCITY
        self.sprite_name = SPRITE_RUN_PREFIX + "1"
        self.run_sprite_count = 1

        self.game_state = game_state

        self.surf = sprites_images[self.sprite_name]
        self.rect: pygame.rect.Rect = self.surf.get_rect(
            center=(
                WIDTH / 2 + HORIZONTAL_PADDING,
                configs.SCREEN_HEIGHT - floor.HEIGHT - HEIGHT / 2
            )
        )

    def update(self, pressed_keys):

        if pressed_keys[K_UP] and self.is_on_floor():
            self.is_jumping = True
            self.run_sprite_count = 1
            self.surf = sprites_images[SPRITE_RUN_PREFIX + str(self.run_sprite_count)]
            self.process_jump()

        elif pressed_keys[K_DOWN] and self.is_downing:
            self.is_jumping = False
            self.using_accelerate_fall = True
            self.process_fall()

        elif self.is_jumping:
            self.process_jump()

        if self.is_downing:
            self.process_fall()

        else:
            self.run_sprite_count += 1
            if self.run_sprite_count > len(sprites_images):
                self.run_sprite_count = 1

            self.surf = sprites_images[SPRITE_RUN_PREFIX + str(self.run_sprite_count)]

    def is_on_floor(self):
        return self.rect.bottom >= self.game_state.floor_rect.top

    def process_jump(self):
        self.rect.move_ip(0, -self.jump_velocity)
        self.jump_velocity -= configs.GRAVITY
        if self.jump_velocity <= 0:
            self.is_jumping = False
            self.is_downing = True
            self.jump_velocity = INITIAL_JUMP_VELOCITY

    def process_fall(self):
        dumping_value = FALL_DAMPING_VALUE
        if self.using_accelerate_fall:
            dumping_value = 1

        self.rect.move_ip(0, INITIAL_JUMP_VELOCITY * dumping_value)
        if self.is_on_floor():
            self.rect.move_ip(0, -max(0, self.rect.bottom - self.game_state.floor_rect.top))
            self.is_jumping = False
            self.is_downing = False
            self.using_accelerate_fall = False
