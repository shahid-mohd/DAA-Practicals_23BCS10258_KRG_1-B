# Window and Grid Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GRID_WIDTH = 50
GRID_HEIGHT = 40
CELL_SIZE = 20

# Frame Rate
FPS = 60

# Colors (RGB)
COLOR_BACKGROUND = (15, 15, 25)
COLOR_GRID_LINE = (40, 40, 50)
COLOR_WALL = (30, 30, 40)
COLOR_EMPTY = (240, 240, 245)
COLOR_START = (46, 204, 113)
COLOR_END = (231, 76, 60)
COLOR_PATH = (241, 196, 15)
COLOR_VISITED = (52, 152, 219)
COLOR_FRONTIER = (155, 89, 182)
COLOR_TEXT = (236, 240, 241)

# Animation Settings
ANIMATION_SPEED_MIN = 1
ANIMATION_SPEED_MAX = 100
ANIMATION_SPEED_DEFAULT = 20

# Maze Cell Types
CELL_EMPTY = 0
CELL_WALL = 1
CELL_START = 2
CELL_END = 3
CELL_PATH = 4

# Direction Vectors (for pathfinding)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
DIRECTIONS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Including diagonals
