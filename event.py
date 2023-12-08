import random
import time

import pygame
import tree

import state
import cloud

ADDTREE = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2


class EventManager:

    def __init__(self, game_state: state.GameState):
        self.game_state = game_state
        self.last_rendered_tree_timestamp = time.time() * 1000
        self.tree_render_delay = random.randint(500, 1000)

        pygame.time.set_timer(ADDCLOUD, 1000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.stop_game()

            if event.type == ADDTREE:
                new_tree = tree.Tree(self.game_state.dino_rect, self.game_state)
                self.game_state.all_sprites_group.add(new_tree)
                self.game_state.trees_sprites_group.add(new_tree)

            if event.type == ADDCLOUD:
                new_cloud = cloud.Cloud()
                self.game_state.all_sprites_group.add(new_cloud)

    def produce_events(self):
        time.time()
        if ((time.time() * 1000) - self.last_rendered_tree_timestamp) > self.tree_render_delay:
            self.last_rendered_tree_timestamp = time.time() * 1000
            self.tree_render_delay = random.randint(600, 1200)
            pygame.event.post(pygame.event.Event(ADDTREE))
