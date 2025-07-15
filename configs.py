SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRAVITY = 0.6  
INITIAL_JUMP_VELOCITY = 12
BASE_GAME_SPEED = 6  # Base speed (pixels per frame)
SPEED_INCREASE_RATE = 0.03  # Speed increases by 0.03 every 30 points (0.001 * 30)

CLOCK_TICK = 60

# Game speed configuration
BASE_TREE_SPEED = BASE_GAME_SPEED  # Use base speed
BASE_CLOUD_SPEED = 0.5  # Clouds move slower

# Animation speed
ANIMATION_FRAMES_PER_SECOND = 12  # Animation speed

# Spawn mechanics
MIN_CACTUS_DISTANCE = 200  # Minimum distance between cacti
MAX_CACTUS_DISTANCE = 600  # Maximum distance between cacti
CACTUS_SPAWN_CHANCE = 0.02  # 2% chance per frame to spawn cactus

# Parallax cloud system
CLOUD_PARALLAX_RATIO = 0.3  # Clouds move at 30% of game speed for parallax effect
MIN_CLOUD_DISTANCE = 300  # Minimum distance between clouds
MAX_CLOUD_DISTANCE = 800  # Maximum distance between clouds
CLOUD_SPAWN_CHANCE = 0.005  # 0.5% chance per frame to spawn cloud
