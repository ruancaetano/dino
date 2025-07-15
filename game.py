import time

import pygame

import controller
import dino
import event
import floor
import colors
import configs
import state
import cloud

# Import constants for collision detection
from dino import DINO_WIDTH, DINO_HEIGHT


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
        self.font = pygame.font.Font(None, 36)
        self.fps_font = pygame.font.Font(None, 24)  # Smaller font for FPS

        self.screen = pygame.display.set_mode([configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT])

    def setup(self):
        self.game_state = state.GameState()

        self.floor_sprite = floor.Floor()
        self.game_state.all_sprites_group.add(self.floor_sprite)
        self.game_state.floor_rect = self.floor_sprite.rect

        for index in range(self.dinos_quantities):
            dino_controller = controller.KeyboardController()

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

            self.draw_hud()

            pygame.display.update()

            # Get FPS and tick the clock
            fps = self.clock.get_fps()
            self.clock.tick(self.game_state.get_tick())

    def draw_hud(self):
        # Draw score
        score_text = self.font.render(f"Score: {self.game_state.max_point}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw current speed (increases every 30 points)
        speed_level = max(0, (self.game_state.max_point - 1) // 30)  # Start level 1 at score 30
        current_speed = configs.BASE_GAME_SPEED + (speed_level * configs.SPEED_INCREASE_RATE)
        speed_text = self.font.render(f"Speed: {current_speed:.1f} (Level: {speed_level})", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 50))
        
        # Draw FPS
        fps = self.clock.get_fps()
        fps_text = self.fps_font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 90))
        
        # Draw top 5 scores on the right side
        self.draw_top_scores()
    
    def draw_top_scores(self):
        """Draw the top 5 dino scores on the right side of the screen"""
        # Get all dino scores and sort them
        scores = [(dino_id, score) for dino_id, score in self.game_state.points.items()]
        scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score (highest first)
        
        # Take top 5
        top_scores = scores[:5]
        
        if not top_scores:
            return
        
        # Position on right side
        start_x = configs.SCREEN_WIDTH - 180
        start_y = 10
        
        # Draw background box
        background_rect = pygame.Rect(start_x - 10, start_y - 5, 190, len(top_scores) * 25 + 20)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), background_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), background_rect, 2)
        
        # Draw title
        title_font = pygame.font.Font(None, 24)
        title_text = title_font.render("TOP 5", True, (255, 255, 255))
        self.screen.blit(title_text, (start_x, start_y))
        
        # Draw scores
        score_font = pygame.font.Font(None, 20)
        for i, (dino_id, score) in enumerate(top_scores):
            y_pos = start_y + 25 + (i * 20)
            
            # Score text with rank
            rank = i + 1
            score_text = score_font.render(f"#{rank} Dino {dino_id}: {score}", True, (255, 255, 255))
            self.screen.blit(score_text, (start_x, y_pos))

    pygame.quit()

    def verify_collisions(self):
        sprites_to_delete = []

        for index, sprite in enumerate(self.dino_sprites):
            # Update collision rect position
            sprite.update_collision_rect()
            
            # Check collision with smaller collision box
            collision = False
            for tree_sprite in self.game_state.trees_sprites_group:
                if sprite.collision_rect.colliderect(tree_sprite.rect):
                    collision = True
                    break
            
            if collision:
                sprite.kill()
                sprites_to_delete.append(index)

        for to_delete_index in sorted(sprites_to_delete, reverse=True):
            self.dino_sprites.pop(to_delete_index)
            self.dinos_quantities -= 1

        if len(self.dino_sprites) == 0:
            self.screen.fill(colors.RED_RGB)
            self.game_state.stop_game()

    def update_sprites(self):
        # Calculate current game speed for parallax (increases every 30 points)
        speed_level = max(0, (self.game_state.max_point - 1) // 30)  # Start level 1 at score 30
        current_speed = configs.BASE_GAME_SPEED + (speed_level * configs.SPEED_INCREASE_RATE)

        # Update floor with parallax scrolling
        self.floor_sprite.update(current_speed)
        # Render both floor segments for seamless tiling
        self.screen.blit(self.floor_sprite.surf, self.floor_sprite.rect)
        self.screen.blit(self.floor_sprite.surf2, self.floor_sprite.rect2)

        # Update and draw all sprites
        for entity in self.game_state.all_sprites_group:
            if hasattr(entity, 'update') and callable(getattr(entity, 'update')):
                # Check if it's a cloud and needs special update
                if isinstance(entity, cloud.Cloud):
                    entity.update(current_speed)
                else:
                    entity.update()
            self.screen.blit(entity.surf, entity.rect)


