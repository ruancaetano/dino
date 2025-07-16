import random
import numpy as np
import copy
from typing import List, Tuple
import network

class GeneticAlgorithm:
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.generation = 0
        self.best_fitness = 0
        self.best_individual = None
        
    def initialize_population(self, input_size: int, hidden_layers: int, hidden_nodes: int, output_size: int):
        self.population = []
        
        best_individual = self.load_best_individual()
        
        for i in range(self.population_size):
            nn = network.NeuralNetwork(input_size, hidden_layers, hidden_nodes, output_size)
            
            if i == 0 and best_individual is not None:
                nn.load_weights(best_individual.get_weights())
                print(f"Loaded best individual (Gen {self.generation}, Fitness: {self.best_fitness}) as starting point")
            
            self.population.append(nn)
        
        print(f"Initialized population of {self.population_size} neural networks")
    
    def load_best_individual(self, filename: str = "best_genetic_dino.npz"):
        try:
            data = np.load(filename)
            num_weights = data['num_weights']
            
            nn = network.NeuralNetwork(6, 3, 5, 2) 
            
            weights = []
            for i in range(num_weights):
                weights.append(data[f'weight_{i}'])
            
            nn.load_weights(weights)
            
            self.generation = data['generation']
            self.best_fitness = data['fitness']
            self.best_individual = nn
            
            print(f"Loaded best genetic individual (Gen {self.generation}, Fitness: {self.best_fitness}) from {filename}")
            return nn
            
        except Exception as e:
            print(f"No previous training file found, starting with random weights")
            return None
    
    def evaluate_fitness(self, individual: network.NeuralNetwork, game_results: List[Tuple[int, int]]) -> float:
        for dino_id, score in game_results:
            if dino_id - 1 < len(self.population) and self.population[dino_id - 1] is individual:
                return float(score)
        return 0.0
    
    def select_parents(self, fitness_scores: List[float]) -> Tuple[network.NeuralNetwork, network.NeuralNetwork]:
        """Select two parents using tournament selection"""
        tournament_size = 3
        
        def tournament_select():
            tournament = random.sample(range(len(self.population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament]
            winner_idx = tournament[tournament_fitness.index(max(tournament_fitness))]
            return self.population[winner_idx]
        
        parent1 = tournament_select()
        parent2 = tournament_select()
        
        return parent1, parent2
    
    def crossover(self, parent1: network.NeuralNetwork, parent2: network.NeuralNetwork) -> network.NeuralNetwork:
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1)
        
        child = copy.deepcopy(parent1)
        parent2_weights = parent2.get_weights()
        child_weights = child.get_weights()
        
        # Perform uniform crossover on weights
        for i in range(len(child_weights)):
            if random.random() < 0.5:
                child_weights[i] = parent2_weights[i].copy()
        
        child.load_weights(child_weights)
        return child
    
    def mutate(self, individual: network.NeuralNetwork):
        if random.random() > self.mutation_rate:
            return
        
        weights = individual.get_weights()
        
        for i in range(len(weights)):
            if random.random() < 0.1:  # 10% chance to mutate each weight array
                # Add random noise to weights
                noise = np.random.normal(0, 0.1, weights[i].shape)
                weights[i] += noise
                # Clip weights to match initialization range (-1, 1)
                weights[i] = np.clip(weights[i], -1, 1)
        
        individual.load_weights(weights)
    
    def evolve(self, game_results: List[Tuple[int, int]]) -> List[network.NeuralNetwork]:
        self.generation += 1
        
        fitness_scores = []
        for i, individual in enumerate(self.population):
            fitness = self.evaluate_fitness(individual, game_results)
            fitness_scores.append(fitness)
        
        best_idx = fitness_scores.index(max(fitness_scores))
        best_fitness = fitness_scores[best_idx]
        
        if best_fitness > self.best_fitness:
            self.best_fitness = best_fitness
            self.best_individual = copy.deepcopy(self.population[best_idx])
            print(f"New best fitness: {self.best_fitness} (Generation {self.generation})")
        
        print(f"Generation {self.generation} - Best: {best_fitness}, Avg: {np.mean(fitness_scores):.1f}")
        
        new_population = []
        
        # Elitism: keep the best individual
        new_population.append(copy.deepcopy(self.population[best_idx]))
        
        # Generate rest of population through selection, crossover, and mutation
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents(fitness_scores)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        
        self.population = new_population
        return self.population
    
    def get_best_individual(self) -> network.NeuralNetwork:
        if self.best_individual is None:
            raise ValueError("No best individual found")
        return self.best_individual
    
    def save_best_individual(self, filename: str = "best_genetic_dino.npz"):
        if self.best_individual is None:
            print(" No best individual to save")
            return False
        
        try:
            weights = self.best_individual.get_weights()
            save_dict = {
                'generation': self.generation,
                'fitness': self.best_fitness,
                'num_weights': len(weights)
            }
            
            for i, weight_array in enumerate(weights):
                save_dict[f'weight_{i}'] = weight_array
            
            np.savez(filename, **save_dict)
            print(f"Saved best genetic individual (Gen {self.generation}, Fitness: {self.best_fitness}) to {filename}")
            return True
        except Exception as e:
            print(f"Error saving best individual: {e}")
            return False
    
 