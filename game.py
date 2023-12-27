import time

import pygame

import controller
import dino
import event
import floor
import colors
import configs
import state


class Game:
    def __init__(self, dinos_quantities: int):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.clock_tick = configs.CLOCK_TICK
        self.dinos_quantities = dinos_quantities
        self.event_manager = None
        self.dino_sprites = []
        self.game_state = None
        self.floor_sprite = None

        self.screen = pygame.display.set_mode([configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT])

    def setup(self):
        self.game_state = state.GameState()

        self.floor_sprite = floor.Floor()
        self.game_state.all_sprites_group.add(self.floor_sprite)
        self.game_state.floor_rect = self.floor_sprite.rect

        for index in range(self.dinos_quantities):
            dino_controller = controller.RandomController()

            dino_id = index + 1
            dino_sprite = dino.Dino(dino_id, self.game_state, dino_controller)
            self.dino_sprites.append(dino_sprite)
            self.game_state.all_sprites_group.add(dino_sprite)
            self.game_state.dino_rects_map[dino_id] = dino_sprite.rect
            self.game_state.points[dino_id] = 0

        self.event_manager = event.EventManager(self.game_state)

        self.game_state.start_game()

    def start(self):
        while self.game_state.running:
            self.screen.fill(colors.BLUE_RGB)

            self.event_manager.produce_events()

            self.event_manager.handle_events()

            self.update_sprites()

            self.verify_collisions()

            pygame.display.update()

            print(self.game_state.points)
            self.clock.tick(self.game_state.get_tick())

    pygame.quit()

    def verify_collisions(self):
        sprites_to_delete = []

        for index, sprite in enumerate(self.dino_sprites):
            if pygame.sprite.spritecollideany(sprite, self.game_state.trees_sprites_group):
                sprite.kill()
                sprites_to_delete.append(index)

        for to_delete_index in sorted(sprites_to_delete, reverse=True):
            self.dino_sprites.pop(to_delete_index)
            self.dinos_quantities -= 1

        if len(self.dino_sprites) == 0:
            self.screen.fill(colors.RED_RGB)
            self.game_state.stop_game()

    def update_sprites(self):
        self.screen.blit(self.floor_sprite.surf, self.floor_sprite.rect)

        for entity in self.game_state.all_sprites_group:
            entity.update()
            self.screen.blit(entity.surf, entity.rect)
