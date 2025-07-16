import random
import time

import pygame

import configs
import floor
import controller

from pygame.locals import (
    K_UP,
    K_DOWN,
)

import state

DINO_WIDTH = 80
DINO_HEIGHT = 70
INITIAL_JUMP_VELOCITY = configs.INITIAL_JUMP_VELOCITY  # Use jump velocity
HORIZONTAL_PADDING = 100
FALL_DAMPING_VALUE = 0.5
SPRITE_RUN_PREFIX = "run-"

# Original sprites (will be colored per dino instance)
original_sprites = {
    SPRITE_RUN_PREFIX + "1": pygame.transform.scale(pygame.image.load("./sprites/run-1.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "2": pygame.transform.scale(pygame.image.load("./sprites/run-2.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "3": pygame.transform.scale(pygame.image.load("./sprites/run-3.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "4": pygame.transform.scale(pygame.image.load("./sprites/run-4.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "5": pygame.transform.scale(pygame.image.load("./sprites/run-5.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "6": pygame.transform.scale(pygame.image.load("./sprites/run-6.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "7": pygame.transform.scale(pygame.image.load("./sprites/run-7.png"), (DINO_WIDTH, DINO_HEIGHT)),
    SPRITE_RUN_PREFIX + "8": pygame.transform.scale(pygame.image.load("./sprites/run-8.png"), (DINO_WIDTH, DINO_HEIGHT))
}


class Dino(pygame.sprite.Sprite):

    def __init__(self, dino_id: int, game_state: state.GameState, dino_controller: controller.Controller):
        super(Dino, self).__init__()
        self.id = dino_id
        self.dino_controller = dino_controller
        self.using_accelerate_fall = False
        self.is_jumping = False
        self.is_downing = False
        self.jump_velocity = INITIAL_JUMP_VELOCITY
        self.fall_velocity = 0  # Track fall velocity separately
        self.sprite_name = SPRITE_RUN_PREFIX + "1"
        self.run_sprite_count = 1
        self.points = 0
        self.last_animation_update = time.time()
        self.animation_interval = 1.0 / configs.ANIMATION_FRAMES_PER_SECOND

        self.game_state = game_state
        
        # Generate random color for this dino
        self.dino_color = self.generate_random_color()
        
        # Create colored sprites for this dino
        self.colored_sprites = self.create_colored_sprites()

        self.surf = self.colored_sprites[self.sprite_name]
        self.rect: pygame.rect.Rect = self.surf.get_rect(
            center=(
               (DINO_WIDTH / 2 + HORIZONTAL_PADDING) - random.randint(0, HORIZONTAL_PADDING),
                configs.SCREEN_HEIGHT - floor.HEIGHT - DINO_HEIGHT / 2
            )
        )
        
        # Create a smaller collision box for better jumping
        self.collision_rect = pygame.Rect(
            int(self.rect.x + DINO_WIDTH * 0.1),  # Even smaller collision box
            int(self.rect.y + DINO_HEIGHT * 0.2),  # Start higher
            int(DINO_WIDTH * 0.8),  # 80% of sprite width
            int(DINO_HEIGHT * 0.6)   # 60% of sprite height
        )

    def generate_random_color(self):
        """Generate a random color for the dino"""
        # Generate bright, vibrant colors
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return (r, g, b)
    
    def create_colored_sprites(self):
        """Create colored versions of all sprites for this dino"""
        colored_sprites = {}
        for sprite_name, original_sprite in original_sprites.items():
            # Create a copy of the original sprite
            colored_sprite = original_sprite.copy()
            
            # Apply color filter
            colored_sprite.fill(self.dino_color, special_flags=pygame.BLEND_MULT)
            
            colored_sprites[sprite_name] = colored_sprite
        
        return colored_sprites

    def update_collision_rect(self):
        """Update collision rect position to match current sprite position"""
        self.collision_rect.x = int(self.rect.x + DINO_WIDTH * 0.1)
        self.collision_rect.y = int(self.rect.y + DINO_HEIGHT * 0.2)

    def update(self):
        self.dino_controller.set_pressed_keys()
        if self.dino_controller.pressed_keys[K_UP] and self.is_on_floor():
            self.is_jumping = True
            self.is_downing = False
            self.jump_velocity = INITIAL_JUMP_VELOCITY
            self.fall_velocity = 0
            self.run_sprite_count = 1
            self.surf = self.colored_sprites[SPRITE_RUN_PREFIX + str(self.run_sprite_count)]
            self.process_jump()

        elif self.dino_controller.pressed_keys[K_DOWN] and (self.is_jumping or self.is_downing):
            self.using_accelerate_fall = True
        else:
            self.using_accelerate_fall = False

        if self.is_jumping:
            self.process_jump()

        if self.is_downing:
            self.process_fall()

        else:
            # Control animation speed
            current_time = time.time()
            if current_time - self.last_animation_update >= self.animation_interval:
                self.run_sprite_count += 1
                if self.run_sprite_count > len(self.colored_sprites):
                    self.run_sprite_count = 1
                self.last_animation_update = current_time

            self.surf = self.colored_sprites[SPRITE_RUN_PREFIX + str(self.run_sprite_count)]

    def is_on_floor(self):
        return self.rect.bottom >= self.game_state.floor_rect.top

    def process_jump(self):
        self.rect.move_ip(0, -self.jump_velocity)
        self.jump_velocity -= configs.GRAVITY
        if self.jump_velocity <= 0:
            self.is_jumping = False
            self.is_downing = True
            self.fall_velocity = 0  # Start fall velocity at 0

    def process_fall(self):
        # Simple gravity falling
        if self.using_accelerate_fall:
            # Accelerate fall when down button is pressed
            self.fall_velocity += configs.GRAVITY * 2
        else:
            # Normal gravity falling
            self.fall_velocity += configs.GRAVITY
        
        self.rect.move_ip(0, self.fall_velocity)
        
        if self.is_on_floor():
            self.rect.move_ip(0, -max(0, self.rect.bottom - self.game_state.floor_rect.top))
            self.is_jumping = False
            self.is_downing = False
            self.using_accelerate_fall = False
            self.fall_velocity = 0
