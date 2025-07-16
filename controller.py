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


class TrainedController(Controller):
    pressed_keys = {K_UP: False, K_DOWN: False}
    
    def __init__(self):
        super().__init__()
        self.model_loaded = False
        self.load_trained_model()
    
    def load_trained_model(self):
        """Load the last trained model (placeholder for future implementation)"""
        try:
            # TODO: Implement model loading from saved file
            # For now, this acts like a random controller
            print("🤖 Trained model loaded (placeholder)")
            self.model_loaded = True
        except Exception as e:
            print(f"⚠️ Could not load trained model: {e}")
            print("🤖 Falling back to random controller")
            self.model_loaded = False
    
    def set_pressed_keys(self):
        """Use trained model to make decisions"""
        if self.model_loaded:
            # TODO: Implement actual model prediction
            # For now, use improved random logic
            import random
            # More intelligent random behavior (jump more often when needed)
            if random.random() < 0.7:  # 70% chance to jump
                self.pressed_keys[K_UP] = True
                self.pressed_keys[K_DOWN] = False
            else:
                self.pressed_keys[K_UP] = False
                self.pressed_keys[K_DOWN] = random.random() < 0.3
        else:
            # Fallback to random controller
            random_index = random.randint(0, 1)
            for key, value in self.pressed_keys.items():
                if key == [K_UP, K_DOWN][random_index]:
                    self.pressed_keys[key] = True
                else:
                    self.pressed_keys[key] = False
