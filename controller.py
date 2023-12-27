import random

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
)


class Controller:
    pressed_keys = {}

    def set_pressed_keys(self):
        pass


class KeyboardController(Controller):
    pressed_keys = {}

    def set_pressed_keys(self):
        self.pressed_keys = pygame.key.get_pressed()


class RandomController(Controller):
    pressed_keys = {K_UP: False, K_DOWN: False}
    options = [K_UP, K_DOWN]

    def set_pressed_keys(self):
        random_index = random.randint(0, 1)
        for key, value in self.pressed_keys.items():
            if key == self.options[random_index]:
                self.pressed_keys[key] = True
                continue
            self.pressed_keys[key] = False
