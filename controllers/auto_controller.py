import random
import numpy as np

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
)

from controllers.controller import Controller
from train import network
from game import state



class AutoController(Controller):
    pressed_keys = {K_UP: False, K_DOWN: False}

    def __init__(self, dino_id: int, game_state: state.GameState):
        super().__init__()
        self.dino_id = dino_id
        self.game_state = game_state
        self.rna = network.NeuralNetwork(6, 3, 5, 2)
        
        # Try to load the best genetic individual if available
        self.load_best_genetic_weights()

    def set_pressed_keys(self):
        inputs = self.game_state.get_neural_network_inputs(self.dino_id)
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