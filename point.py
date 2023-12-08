import pygame

import colors
import configs
import state

WIDTH = 120
HEIGHT = 60

sysfont = pygame.font.get_default_font()
class Point:
    def __init__(self, game_state: state.GameState):
        self.font = pygame.font.SysFont(sysfont, 30)
        self.game_state = game_state
        self.img = self.font.render(str(self.game_state.points), True, colors.RED_RGB)
        self.rect = (
            configs.SCREEN_WIDTH - WIDTH,
            HEIGHT / 2
        )

    def update(self):
        self.img = self.font.render(f"Level {self.game_state.level}: {self.game_state.points}",
                                    True,
                                    colors.BLACK_RGB)
