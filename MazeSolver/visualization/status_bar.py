"""Status bar component for displaying algorithm statistics and messages."""

import pygame
from typing import Optional, Dict
from utils.constants import COLOR_TEXT, COLOR_BACKGROUND


class StatusBar:
    """Display algorithm statistics and status messages."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width - 400, height)
        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 24)

        self.status_message = ""
        self.message_timer = 0.0
        self.message_duration = 1.0  # seconds

    def set_status(self, message: str):
        """Set a temporary status message."""
        self.status_message = message
        self.message_timer = self.message_duration

    def update(self, dt: float):
        """Update status message timer."""
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.status_message = ""

    def render(self, screen: pygame.Surface, stats: Optional[Dict] = None):
        """Render status bar with stats and messages."""
        # Draw background
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2)

        y_offset = self.rect.y + 15

        # Show status message if active
        if self.status_message:
            text = self.font.render(self.status_message, True, COLOR_TEXT)
            screen.blit(text, (self.rect.x + 20, y_offset))
            return

        # Show stats if algorithm finished
        if stats:
            stat_items = [
                f"Algorithm: {stats['algorithm_name']}",
                f"Time: {stats['time_taken']:.4f}s",
                f"Nodes Explored: {stats['nodes_explored']}",
                f"Path Length: {stats['path_length']}" if stats['path_found'] else "No Path Found"
            ]

            x_start = self.rect.x + 20
            spacing = (self.rect.width - 40) // len(stat_items)

            for i, item in enumerate(stat_items):
                text = self.small_font.render(item, True, COLOR_TEXT)
                screen.blit(text, (x_start + i * spacing, y_offset + 5))
        else:
            # Default message
            text = self.small_font.render("Ready", True, COLOR_TEXT)
            screen.blit(text, (self.rect.x + 20, y_offset + 5))
