import pygame

import colors
import configs
import state


class Point:
    def __init__(self, game_state: state.GameState):
        self.game_state = game_state

    def update(self):
        for dino_id, point in self.game_state.points.items():
            if point > 0:
                print(f"Dino {dino_id}:{point}")


