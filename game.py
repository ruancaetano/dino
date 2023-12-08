import pygame

import dino
import event
import floor
import colors
import configs
import point
import state


class Game:
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        self.clock_tick = configs.CLOCK_TICK
        self.game_points = None
        self.event_manager = None
        self.dino_sprite = None
        self.game_state = None
        self.floor_sprite = None

        self.screen = pygame.display.set_mode([configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT])

    def setup(self):
        self.game_state = state.GameState()

        self.floor_sprite = floor.Floor()
        self.game_state.all_sprites_group.add(self.floor_sprite)
        self.game_state.floor_rect = self.floor_sprite.rect

        self.dino_sprite = dino.Dino(self.game_state)
        self.game_state.all_sprites_group.add(self.dino_sprite)
        self.game_state.dino_rect = self.dino_sprite.rect

        self.game_points = point.Point(self.game_state)

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

            self.clock.tick(self.game_state.get_tick())

    pygame.quit()

    def verify_collisions(self):
        if pygame.sprite.spritecollideany(self.dino_sprite, self.game_state.trees_sprites_group):
            self.dino_sprite.kill()
            self.screen.fill(colors.RED_RGB)
            self.game_state.stop_game()

    def update_sprites(self):
        self.game_points.update()
        self.screen.blit(self.game_points.img, self.game_points.rect)
        self.screen.blit(self.floor_sprite.surf, self.floor_sprite.rect)

        pressed_keys = pygame.key.get_pressed()

        for entity in self.game_state.all_sprites_group:
            entity.update(pressed_keys)
            self.screen.blit(entity.surf, entity.rect)
