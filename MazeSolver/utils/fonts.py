import pygame
import os


class FontManager:
    """Manages fonts for the application."""

    _fonts = {}

    @staticmethod
    def init():
        """Initialize fonts."""
        pygame.font.init()

    @staticmethod
    def get_font(size: int = 24, bold: bool = False) -> pygame.font.Font:
        """Get a font with caching."""
        key = (size, bold)

        if key not in FontManager._fonts:
            font = pygame.font.SysFont('Arial', size, bold=bold)
            if not font:
                font = pygame.font.Font(None, size)
            FontManager._fonts[key] = font

        return FontManager._fonts[key]
