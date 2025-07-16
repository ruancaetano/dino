import random
import numpy as np
import pygame
from pygame.locals import K_UP, K_DOWN
import network
import state
import configs
import genetic_algorithm

class GeneticController:
    pressed_keys = {K_UP: False, K_DOWN: False}

    def __init__(self, dino_id: int, game_state: state.GameState, neural_network: network.NeuralNetwork):
        self.dino_id = dino_id
        self.game_state = game_state
        self.rna = neural_network

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

class GeneticGameManager:
    def __init__(self, population_size: int = 50):
        self.ga = genetic_algorithm.GeneticAlgorithm(population_size=population_size)
        self.ga.initialize_population(3, 3, 5, 2)  # 3 inputs, 3 hidden layers, 5 nodes, 2 outputs
        self.current_generation = 0
        self.games_per_generation = 3  # Number of games to play before evolving
        
    def get_controllers_for_game(self, num_dinos: int, game_state: state.GameState):
        """Get genetic controllers for a new game"""
        controllers = []
        for i in range(num_dinos):
            if i < len(self.ga.population):
                neural_network = self.ga.population[i]
                controller = GeneticController(i + 1, game_state, neural_network)
                controllers.append(controller)
            else:
                # If we need more controllers than population size, use random ones
                neural_network = network.NeuralNetwork(3, 3, 5, 2)
                controller = GeneticController(i + 1, game_state, neural_network)
                controllers.append(controller)
        return controllers
    
    def evolve_population(self, game_results):
        """Evolve the population based on game results"""
        self.ga.evolve(game_results)
        self.current_generation += 1
        
        # Save the best individual periodically
        if self.current_generation % 10 == 0:
            self.ga.save_best_individual()
    
    def get_best_individual(self):
        """Get the best individual from the genetic algorithm"""
        return self.ga.get_best_individual()
    
 