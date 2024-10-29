import random
from typing import List

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
            self.weights = np.random.rand(left_connections)

    def set_output(self, output: float):
        self.output = output

    def calculate_output(self, inputs: np.ndarray):
        self.output = relu(np.dot(self.weights, inputs))
        return self.output

    def randomize_weights(self):
        for i in range(int(random.randint(0, 32767) % len(self.weights))):
            if random.random() < 0.25:
                self.weights[i] *= random.uniform(-0.5, 0.5)
            elif random.random() > 0.50:
                self.weights[i] += random.uniform(-0.5, 0.5)
            else:
                self.weights[i] = random.uniform(-0.5, 0.5)

    def set_weights(self, weights: np.array):
        self.weights = weights


class Layer:
    neurons: List[Neuron]

    def __init__(self, neurons_count: int, left_connections: int):
        self.neurons = []
        for i in range(neurons_count):
            self.neurons.append(Neuron(left_connections))

    def get_outputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.output)
        return np.array(outputs)


class NeuralNetwork:

    def __init__(self, input_layer_nodes: int, hidden_layers: int, hidden_layers_node: int, output_nodes: int):
        self.input_layer_nodes = input_layer_nodes + BIAS
        self.hidden_layers_count = hidden_layers
        self.hidden_layers_nodes_count = hidden_layers_node + BIAS
        self.output_nodes_count = output_nodes

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
        self.output_layer = Layer(self.output_nodes_count, self.hidden_layers_nodes_count)

    def calculate_output(self, inputs: List[float]):
        for idx, input_value in enumerate(inputs):
            self.input_layer.neurons[idx].set_output(input_value)

        # input to first hidden layer
        next_inputs = []
        inputs = self.input_layer.get_outputs()
        for hidden_layer in self.hidden_layers:
            for idx in range(len(hidden_layer.neurons) - BIAS):
                neuron = hidden_layer.neurons[idx]
                neuron.calculate_output(inputs)
            inputs = hidden_layer.get_outputs()

        output = []
        for output_neuron in self.output_layer.neurons:
            output.append(output_neuron.calculate_output(inputs))

        return output

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
                weights.append(neuron.weights)

        for output_neuron in self.output_layer.neurons:
            weights.append(output_neuron.weights)

        return weights

    def load_weights(self, weights: np.array):
        weights_idx = 0
        for hidden_layer in self.hidden_layers:
            for neuron in hidden_layer.neurons:
                neuron.set_weights(weights[weights_idx])
                weights_idx += 1

        for output_neuron in self.output_layer.neurons:
            output_neuron.weights = weights[weights_idx]
            weights_idx += 1
