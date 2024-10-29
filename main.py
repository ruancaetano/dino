import json

import numpy as np

import controller
import game
import network

if __name__ == '__main__':
    generation = 1
    last_best_point = -1
    last_best_weights = None

    while True:
        # init
        dinoCount = 100
        game_obj = game.Game(dinoCount)
        game_obj.setup()

        # configure rna
        if last_best_weights is not None:
            for dino_id in game_obj.dino_controllers:
                controller = game_obj.dino_controllers[dino_id]
                controller.rna.load_weights(last_best_weights)
                if dino_id > dinoCount * 0.25:
                    controller.rna.randomize_weights()

        # start game
        game_obj.start()

        # collect best dino rna weights
        best_dino_controller, best_point = game_obj.get_best_dino()

        if best_point > last_best_point:
            last_best_point = best_point
            last_best_weights = best_dino_controller.rna.get_weights()
            print(last_best_weights)

        print(f'Geração {generation} - Pontuação: {best_point} - Melhor pontuação {last_best_point}')
        generation += 1
