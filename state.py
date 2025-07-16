import pygame
import configs
import floor

# Constants to avoid circular imports
DINO_HEIGHT = 70


class GameState:
    running = False
    dino_rects_map = {}
    floor_rect: pygame.rect.Rect | None = None

    def __init__(self):
        self.points = {}
        self.max_point = 0
        self.all_sprites_group = pygame.sprite.Group()
        self.trees_sprites_group = pygame.sprite.Group()

    def add_point(self, dino_id: int):
        self.points[dino_id] += 1
        if self.points[dino_id] > self.max_point:
            self.max_point = self.points[dino_id]



    def start_game(self):
        self.running = True

    def stop_game(self):
        self.running = False

    def get_tick(self):
        # Constant frame rate, speed increases through obstacle movement
        return configs.CLOCK_TICK

    def get_neural_network_inputs(self, dino_id: int):
        """Extract neural network inputs for a specific dino"""
        dino_rect = self.dino_rects_map[dino_id]
        dino_x = dino_rect.x
        dino_y = dino_rect.y
        
        # Get dino instance to access its state
        dino = None
        for sprite in self.all_sprites_group.sprites():
            if hasattr(sprite, 'id') and sprite.id == dino_id:
                dino = sprite
                break
        
        trees = self.trees_sprites_group.sprites()

        next_target_x = configs.SCREEN_WIDTH
        has_tree_value = 0
        for tree in trees:
            if tree.rect.x > dino_x:
                has_tree_value = 1
                next_target_x = tree.rect.x
                break

        # Calculate dino's vertical position relative to ground
        ground_y = configs.SCREEN_HEIGHT - floor.HEIGHT - DINO_HEIGHT / 2
        vertical_position = (ground_y - dino_y) / ground_y  # Normalized 0-1
        
        # Get dino's vertical velocity
        vertical_velocity = 0
        if dino:
            if dino.is_jumping:
                vertical_velocity = dino.jump_velocity / configs.INITIAL_JUMP_VELOCITY  # Normalized
            elif dino.is_downing:
                vertical_velocity = -dino.fall_velocity / configs.INITIAL_JUMP_VELOCITY  # Normalized negative
        
        # Dino state (0=ground, 1=jumping, 2=falling)
        dino_state = 0
        if dino:
            if dino.is_jumping:
                dino_state = 1
            elif dino.is_downing:
                dino_state = 2
        
        # Game speed level
        speed_level = max(0, (self.max_point - 1) // 20)
        normalized_speed = speed_level / 10  # Normalize to 0-1 range
        
        # Distance to next tree (normalized)
        distance_to_tree = abs(next_target_x - dino_x) / configs.SCREEN_WIDTH

        return [
            has_tree_value,           # 0 or 1 - tree presence
            vertical_position,        # 0-1 - dino's height relative to ground
            vertical_velocity,        # -1 to 1 - normalized vertical velocity
            dino_state,              # 0, 1, or 2 - ground, jumping, falling
            normalized_speed,         # 0-1 - game speed level
            distance_to_tree          # 0-1 - normalized distance to next tree
        ]
