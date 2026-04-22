"""
Configuration file for the drone swarm game.
Contains all game constants and default values.
"""

# Window settings - fullscreen at 1080p
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60
BACKGROUND_COLOR = (20, 20, 30)

# Drone settings
NUM_DRONES = 30
DRONE_SIZE = 5
DRONE_COLOR = (100, 200, 255)
MAX_SPEED = 4.0
MAX_FORCE = 0.1

# Boids algorithm default values
DEFAULT_SEPARATION = 1.5
DEFAULT_ALIGNMENT = 1.0
DEFAULT_COHESION = 1.0
PERCEPTION_RADIUS = 50

# Pathway settings
PATHWAY_WIDTH = 150
PATHWAY_SEGMENT_LENGTH = 200
NUM_SEGMENTS = 5
PATHWAY_COLOR = (50, 50, 50)
GATE_COLOR = (100, 255, 100)
GATE_THICKNESS = 5

# UI settings
SLIDER_WIDTH = 250
SLIDER_HEIGHT = 20
SLIDER_X = 50
SLIDER_Y_START = 50
SLIDER_SPACING = 100
SLIDER_COLOR = (100, 100, 100)
SLIDER_HANDLE_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24

# Slider ranges
SEPARATION_RANGE = (0.0, 3.0)
ALIGNMENT_RANGE = (0.0, 2.0)
COHESION_RANGE = (0.0, 2.0)

# Game settings
GOAL_RADIUS = 30
GOAL_COLOR = (255, 200, 50)
SUCCESS_THRESHOLD = 0.8  # 80% of drones need to reach goal

# Difficulty Levels
DIFFICULTY_LEVELS = {
    'easy': {
        'name': 'Easy',
        'num_drones': 20,
        'num_segments': 5,
        'pathway_width': 170,
        'separation_range': (0.3, 3.5),
        'alignment_range': (0.0, 3.5),
        'cohesion_range': (0.0, 1.2),
        'seek_weight': 0.3,
        'success_threshold': 0.7,
    },
    'medium': {
        'name': 'Medium',
        'num_drones': 30,
        'num_segments': 5,
        'pathway_width': 150,
        'separation_range': (0.0, 3.0),
        'alignment_range': (0.0, 3.0),
        'cohesion_range': (0.0, 1.5),
        'seek_weight': 0.25,
        'success_threshold': 0.8,
    },
    'hard': {
        'name': 'Hard',
        'num_drones': 15,
        'num_segments': 7,
        'pathway_width': 80,
        'separation_range': (0.0, 2.0),
        'alignment_range': (0.0, 2.5),
        'cohesion_range': (0.0, 1.5),
        'seek_weight': 0.15,
        'success_threshold': 0.9,
    },
}
