import pygame
from typing import List, Dict, Tuple
from maze.grid import Grid
from algorithms import AlgorithmFactory
from utils.constants import *


class ComparisonView:
    """Compare multiple algorithms side-by-side."""

    def __init__(self, screen: pygame.Surface, algorithms: List[str]):
        self.screen = screen
        self.algorithms = algorithms
        self.grids = []
        self.results = []
        self.running = False

        # Layout
        self.num_algorithms = len(algorithms)
        self.grid_width = WINDOW_WIDTH // self.num_algorithms
        self.cell_size = min(15, self.grid_width // GRID_WIDTH)

        # Create separate grids for each algorithm
        for _ in algorithms:
            grid = Grid(GRID_HEIGHT, GRID_WIDTH)
            grid.set_start(1, 1)
            grid.set_end(GRID_HEIGHT - 2, GRID_WIDTH - 2)
            self.grids.append(grid)

        self.font = pygame.font.Font(None, 20)

    def load_maze(self, maze_data: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
        """Load same maze into all grids."""
        for grid in self.grids:
            grid.load_from_array(maze_data, start, end)

    def run_comparison(self):
        """Run all algorithms and collect results."""
        self.results = []

        for i, (grid, algo_name) in enumerate(zip(self.grids, self.algorithms)):
            algorithm = AlgorithmFactory.create(algo_name, grid)
            path, stats = algorithm.find_path()

            self.results.append({
                'algorithm': algo_name,
                'path': path,
                'stats': stats,
                'grid': grid
            })

            print(f"Completed: {algo_name.upper()}")

    def render(self):
        """Render comparison view."""
        self.screen.fill(COLOR_BACKGROUND)

        for i, result in enumerate(self.results):
            x_offset = i * self.grid_width
            self._render_grid(result['grid'], x_offset, 100)
            self._render_stats(result, x_offset, 50)

    def _render_grid(self, grid: Grid, x_offset: int, y_offset: int):
        """Render a single grid."""
        for row in grid.cells:
            for cell in row:
                x = x_offset + cell.col * self.cell_size + 10
                y = y_offset + cell.row * self.cell_size

                color = self._get_cell_color(cell)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, COLOR_GRID_LINE, rect, 1)

    def _get_cell_color(self, cell):
        """Get color for cell."""
        if cell.type == CELL_WALL:
            return COLOR_WALL
        elif cell.type == CELL_START:
            return COLOR_START
        elif cell.type == CELL_END:
            return COLOR_END
        elif cell.in_path:
            return COLOR_PATH
        elif cell.visited:
            return COLOR_VISITED
        return COLOR_EMPTY

    def _render_stats(self, result: Dict, x_offset: int, y_offset: int):
        """Render statistics for algorithm."""
        stats = result['stats']

        lines = [
            f"{stats['algorithm'].upper()}",
            f"Time: {stats.get('time_formatted', 'N/A')}",
            f"Nodes: {stats.get('nodes_explored', 0)}",
            f"Path: {stats.get('path_length', 0)}"
        ]

        for i, line in enumerate(lines):
            text = self.font.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (x_offset + 10, y_offset + i * 20))
