import pygame
from pygame.locals import K_UP, K_DOWN
from controllers.controller import Controller

class KeyboardController(Controller):
    pressed_keys = {}

    def set_pressed_keys(self):
        self.pressed_keys = pygame.key.get_pressed()