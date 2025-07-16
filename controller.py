import random
import numpy as np

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
)

import network
import state
import configs


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





class NeuralNetworkController(Controller):
    pressed_keys = {K_UP: False, K_DOWN: False}

    def __init__(self, dino_id: int, game_state: state.GameState):
        super().__init__()
        self.dino_id = dino_id
        self.game_state = game_state
        self.rna = network.NeuralNetwork(3, 3, 5, 2)
        
        # Try to load the best genetic individual if available
        self.load_best_genetic_weights()

    def set_pressed_keys(self):
        dino_x = self.game_state.dino_rects_map[self.dino_id].x
        trees = self.game_state.trees_sprites_group.sprites()

        next_target_x = configs.SCREEN_WIDTH
        has_tree_value = 0
        for tree in trees:
            if tree.rect.x > dino_x:
                has_tree_value = 1
                next_target_x = tree.rect.x
                break

        inputs = [has_tree_value, self.game_state.get_tick(), abs(next_target_x - dino_x)]
        outputs = self.rna.calculate_output(inputs)

        if outputs[0] > 0:
            self.pressed_keys[K_UP] = True
            self.pressed_keys[K_DOWN] = False
            return

        if outputs[1] > 0:
            self.pressed_keys[K_UP] = False
            self.pressed_keys[K_DOWN] = True
            return

        self.pressed_keys[K_UP] = False
        self.pressed_keys[K_DOWN] = False


    def load_best_genetic_weights(self, filename: str = "best_genetic_dino.npz"):
        """Load the best genetic individual's weights"""
        try:
            data = np.load(filename)
            num_weights = data['num_weights']
            
            # Reconstruct the weights list
            weights = []
            for i in range(num_weights):
                weights.append(data[f'weight_{i}'])
            
            self.rna.load_weights(weights)
            print(f"Loaded best genetic individual (Gen {data['generation']}, Fitness: {data['fitness']})")
            return True
        except Exception as e:
            print(f"No genetic training file found, using random weights")
            return False