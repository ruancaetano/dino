import random
from typing import List, Callable

import numpy as np

BIAS = 1

def relu(x):
    return max(0.0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Neuron:
    output: float
    weights: np.ndarray

    def __init__(self, left_connections: int):
        self.output = 1
        if left_connections > 0:
            self.weights = np.random.uniform(-1, 1, left_connections)
        else:
            self.weights = np.array([])

    def set_output(self, output: float):
        self.output = output

    def calculate_output(self, inputs: np.ndarray, activation: Callable[[float], float]):
        if self.weights is not None:
            self.output = activation(np.dot(self.weights, inputs))
        return self.output

    def randomize_weights(self):
        if self.weights is not None:
            self.weights = np.random.uniform(-1, 1, self.weights.shape)

    def set_weights(self, weights: np.ndarray):
        if self.weights is not None and weights.shape == self.weights.shape:
            self.weights = weights.copy()
        else:
            raise ValueError(f"Shape mismatch in set_weights: expected {self.weights.shape}, got {weights.shape}")

class Layer:
    neurons: List[Neuron]

    def __init__(self, neurons_count: int, left_connections: int):
        self.neurons = [Neuron(left_connections) for _ in range(neurons_count)]

    def get_outputs(self):
        return np.array([neuron.output for neuron in self.neurons])

class NeuralNetwork:
    def __init__(self, input_layer_nodes: int, hidden_layers: int, hidden_layers_node: int, output_nodes: int, activation: str = 'relu'):
        self.input_layer_nodes = input_layer_nodes + BIAS
        self.hidden_layers_count = hidden_layers
        self.hidden_layers_nodes_count = hidden_layers_node + BIAS
        self.output_nodes_count = output_nodes
        self.activation = relu if activation == 'relu' else sigmoid

        # create input layer
        self.input_layer = Layer(self.input_layer_nodes, 0)

        # create hidden layers
        self.hidden_layers = []
        for i in range(self.hidden_layers_count):
            if i == 0:
                self.hidden_layers.append(
                    Layer(self.hidden_layers_nodes_count, self.input_layer_nodes)
                )
            else:
                self.hidden_layers.append(
                    Layer(self.hidden_layers_nodes_count, self.hidden_layers_nodes_count)
                )

        # create output layer
        if self.hidden_layers_count > 0:
            self.output_layer = Layer(self.output_nodes_count, self.hidden_layers_nodes_count)
        else:
            self.output_layer = Layer(self.output_nodes_count, self.input_layer_nodes)

    def calculate_output(self, inputs: List[float]):
        # Input validation
        if len(inputs) != self.input_layer_nodes - 1:
            raise ValueError(f"Input size mismatch: expected {self.input_layer_nodes - 1}, got {len(inputs)}")

        # Set input layer outputs
        for idx, input_value in enumerate(inputs):
            self.input_layer.neurons[idx].set_output(input_value)
        # Set bias neuron output
        self.input_layer.neurons[-1].set_output(1)

        # Forward pass through hidden layers
        layer_inputs = self.input_layer.get_outputs()
        for hidden_layer in self.hidden_layers:
            # Set bias neuron output
            for idx in range(len(hidden_layer.neurons) - 1):
                neuron = hidden_layer.neurons[idx]
                neuron.calculate_output(layer_inputs, self.activation)
            hidden_layer.neurons[-1].set_output(1)  # Bias neuron
            layer_inputs = hidden_layer.get_outputs()

        # Output layer
        outputs = []
        for output_neuron in self.output_layer.neurons:
            outputs.append(output_neuron.calculate_output(layer_inputs, self.activation))
        return outputs

    def randomize_weights(self):
        for hidden_layer in self.hidden_layers:
            for neuron in hidden_layer.neurons:
                neuron.randomize_weights()
        for output_neuron in self.output_layer.neurons:
            output_neuron.randomize_weights()

    def get_weights(self):
        weights = []
        for hidden_layer in self.hidden_layers:
            for neuron in hidden_layer.neurons:
                if neuron.weights is not None:
                    weights.append(neuron.weights.copy())
        for output_neuron in self.output_layer.neurons:
            if output_neuron.weights is not None:
                weights.append(output_neuron.weights.copy())
        return weights

    def load_weights(self, weights: List[np.ndarray]):
        idx = 0
        for hidden_layer in self.hidden_layers:
            for neuron in hidden_layer.neurons:
                if neuron.weights is not None:
                    neuron.set_weights(weights[idx])
                    idx += 1
        for output_neuron in self.output_layer.neurons:
            if output_neuron.weights is not None:
                output_neuron.set_weights(weights[idx])
                idx += 1
        if idx != len(weights):
            raise ValueError(f"Weight count mismatch: loaded {idx}, provided {len(weights)}")