import random
import time

import pygame
import tree

import state
import cloud
import configs

ADDTREE = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2


class EventManager:

    def __init__(self, game_state: state.GameState):
        self.game_state = game_state
        self.last_tree_x = configs.SCREEN_WIDTH  # Track last tree position
        self.last_cloud_x = configs.SCREEN_WIDTH  # Track last cloud position
        self.clouds_group = pygame.sprite.Group()  # Separate group for clouds

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.stop_game()

            if event.type == ADDTREE:
                new_tree = tree.Tree(self.game_state)
                self.game_state.all_sprites_group.add(new_tree)
                self.game_state.trees_sprites_group.add(new_tree)
                self.last_tree_x = new_tree.rect.x

            if event.type == ADDCLOUD:
                new_cloud = cloud.Cloud()
                self.game_state.all_sprites_group.add(new_cloud)
                self.clouds_group.add(new_cloud)
                self.last_cloud_x = new_cloud.rect.x

    def produce_events(self):
        # Spawn based on distance and random chance
        if len(self.game_state.trees_sprites_group) == 0:
            # No trees, spawn one
            pygame.event.post(pygame.event.Event(ADDTREE))
        else:
            # Check if we should spawn a new tree based on distance and chance
            last_tree = None
            for tree_sprite in self.game_state.trees_sprites_group:
                if last_tree is None or tree_sprite.rect.x > last_tree.rect.x:
                    last_tree = tree_sprite
            
            if last_tree:
                distance_from_last = configs.SCREEN_WIDTH - last_tree.rect.x
                
                # Spawn logic: random distance + random chance
                should_spawn = (
                    distance_from_last >= configs.MIN_CACTUS_DISTANCE and
                    (distance_from_last >= configs.MAX_CACTUS_DISTANCE or 
                     random.random() < configs.CACTUS_SPAWN_CHANCE)
                )
                
                if should_spawn:
                    pygame.event.post(pygame.event.Event(ADDTREE))
        
        # Parallax cloud spawning
        if len(self.clouds_group) == 0:
            # No clouds, spawn one
            pygame.event.post(pygame.event.Event(ADDCLOUD))
        else:
            # Check if we should spawn a new cloud based on distance and chance
            last_cloud = None
            for cloud_sprite in self.clouds_group:
                if last_cloud is None or cloud_sprite.rect.x > last_cloud.rect.x:
                    last_cloud = cloud_sprite
            
            if last_cloud:
                distance_from_last_cloud = configs.SCREEN_WIDTH - last_cloud.rect.x
                
                # Cloud spawn logic: distance-based + random chance
                should_spawn_cloud = (
                    distance_from_last_cloud >= configs.MIN_CLOUD_DISTANCE and
                    (distance_from_last_cloud >= configs.MAX_CLOUD_DISTANCE or 
                     random.random() < configs.CLOUD_SPAWN_CHANCE)
                )
                
                if should_spawn_cloud:
                    pygame.event.post(pygame.event.Event(ADDCLOUD))

    def update_clouds(self, game_speed):
        # Update all clouds with parallax effect
        for cloud_sprite in self.clouds_group:
            cloud_sprite.update(game_speed)
