"""Handles rendering of the maze and visualizations."""

import pygame
from typing import Optional, List
from maze.grid import Grid
from utils.constants import *
from visualization.animations import ColorTransition, PulseEffect, WaveEffect
from utils.fonts import FontManager

class Visualizer:
    """Handles rendering of the maze and visualization."""

    def __init__(self, screen: pygame.Surface, grid: Grid, layout):
        self.screen = screen
        self.grid = grid
        self.layout = layout
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Animation effects (initialize without parameters - they'll be set when needed)
        self.pulse_effect = PulseEffect(speed=2.0)
        self.wave_effect = None  # Will be created when needed

    def update_animations(self, dt: float):
        """Update animation effects."""
        self.pulse_effect.update(dt)
        if self.wave_effect:
            self.wave_effect.update(dt)

    def render(self, stats_lines: Optional[List[str]] = None):
        """Render the complete visualization."""
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_grid()
        self.draw_cells()
        self.draw_legend()
        self.draw_instructions()

        if stats_lines:
            self.draw_stats(stats_lines)

    def draw_grid(self):
        """Draw grid lines."""
        for row in range(self.grid.rows + 1):
            y = self.layout.grid_y + row * self.layout.cell_size
            pygame.draw.line(
                self.screen,
                COLOR_GRID_LINE,
                (self.layout.grid_x, y),
                (self.layout.grid_x + self.layout.grid_width, y),
                1
            )

        for col in range(self.grid.cols + 1):
            x = self.layout.grid_x + col * self.layout.cell_size
            pygame.draw.line(
                self.screen,
                COLOR_GRID_LINE,
                (x, self.layout.grid_y),
                (x, self.layout.grid_y + self.layout.grid_height),
                1
            )

    # visualizer.py - Update draw_cells method
    def draw_cells(self):
        """Draw all cells with visible grid lines."""
        for row in self.grid.cells:
            for cell in row:
                x, y, w, h = self.layout.get_cell_rect(cell.row, cell.col)

                # Fill cell color
                color = self._get_cell_color(cell)
                pygame.draw.rect(self.screen, color, (x, y, w, h))

                # ALWAYS draw grid lines for better visibility
                pygame.draw.rect(self.screen, COLOR_GRID_LINE, (x, y, w, h), 1)

                # Highlight start/end with thicker border
                if cell == self.grid.start_cell or cell == self.grid.end_cell:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h), 2)

    def _get_cell_color(self, cell):
        """Get color for a cell based on its state."""
        if cell.type == CELL_WALL:
            return COLOR_WALL
        elif cell.type == CELL_START:
            return self.pulse_effect.get_color(COLOR_START)
        elif cell.type == CELL_END:
            return self.pulse_effect.get_color(COLOR_END)
        elif cell.in_path:
            return COLOR_PATH
        elif cell.visited:
            return COLOR_VISITED
        elif cell.in_frontier:
            return COLOR_FRONTIER
        return COLOR_EMPTY

    def draw_legend(self):
        """Draw color legend."""
        legend_x = 20
        legend_y = self.layout.grid_y + self.layout.grid_height + 10

        legend_items = [
            ("Start", COLOR_START),
            ("End", COLOR_END),
            ("Wall", COLOR_WALL),
            ("Visited", COLOR_VISITED),
            ("Frontier", COLOR_FRONTIER),
            ("Path", COLOR_PATH),
        ]

        for i, (label, color) in enumerate(legend_items):
            x = legend_x + i * 120

            # Draw color box
            pygame.draw.rect(self.screen, color, (x, legend_y, 20, 20))
            pygame.draw.rect(self.screen, COLOR_TEXT, (x, legend_y, 20, 20), 1)

            # Draw label
            text = self.small_font.render(label, True, COLOR_TEXT)
            self.screen.blit(text, (x + 25, legend_y + 2))

    def draw_instructions(self):
        """Draw usage instructions in a horizontal layout."""
        instructions = [
            "Ctrl+Click: Set Start",
            "Shift+Click: Set End",
            "Left Click: Draw Wall",
            "Right Click: Erase"
        ]

        start_x = self.layout.grid_x
        y = 15

        for i, line in enumerate(instructions):
            x = start_x + i * 180
            text = self.small_font.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (x, y))

    def draw_stats(self, stats_lines: List[str]):
        """Draw algorithm statistics."""
        x = self.layout.grid_x + self.layout.grid_width + 20
        y = 20

        for i, line in enumerate(stats_lines):
            text = self.font.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (x, y + i * 25))

    def highlight_cell(self, row: int, col: int, color: tuple):
        """Highlight a specific cell."""
        x, y, w, h = self.layout.get_cell_rect(row, col)
        pygame.draw.rect(self.screen, color, (x, y, w, h), 3)

    def draw_path_arrow(self, from_cell, to_cell):
        """Draw arrow from one cell to another."""
        from_x, from_y, w, h = self.layout.get_cell_rect(from_cell.row, from_cell.col)
        to_x, to_y, _, _ = self.layout.get_cell_rect(to_cell.row, to_cell.col)

        # Center points
        start = (from_x + w // 2, from_y + h // 2)
        end = (to_x + w // 2, to_y + h // 2)

        pygame.draw.line(self.screen, COLOR_PATH, start, end, 2)
