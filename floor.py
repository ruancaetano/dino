import pygame

import configs

HEIGHT = 130


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super(Floor, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("sprites/floor.png"), (configs.SCREEN_WIDTH, HEIGHT))
        
        # Position the floor to align properly with dino and trees
        self.rect = self.surf.get_rect(
            bottom=configs.SCREEN_HEIGHT  # Align bottom of floor with bottom of screen
        )
        
        # Parallax scrolling properties
        self.scroll_x = 0
        self.scroll_speed = 1.0  # Floor moves at same speed as trees for consistency
        
        # Create a second floor segment for seamless tiling
        self.surf2 = pygame.transform.scale(pygame.image.load("sprites/floor.png"), (configs.SCREEN_WIDTH, HEIGHT))
        self.rect2 = self.surf2.get_rect(
            bottom=configs.SCREEN_HEIGHT,
            left=configs.SCREEN_WIDTH  # Start second segment right after the first
        )
    
    def update(self, game_speed=0):
        """Update floor position for parallax scrolling with seamless tiling"""
        # Move floor segments to the left to create forward movement sensation
        self.scroll_x -= game_speed * self.scroll_speed
        
        # Update the first floor segment position
        self.rect.x = self.scroll_x
        
        # Update the second floor segment position
        self.rect2.x = self.scroll_x + configs.SCREEN_WIDTH
        
        # Reset positions when segments have moved completely off screen
        if self.scroll_x <= -configs.SCREEN_WIDTH:
            self.scroll_x = 0
            self.rect.x = 0
            self.rect2.x = configs.SCREEN_WIDTH
