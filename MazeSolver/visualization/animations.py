"""Animation effects for visualizations."""

import pygame
import math
from typing import Tuple


class ColorTransition:
    """Smoothly transition between colors."""

    def __init__(self, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int], duration: float = 1.0):
        self.start_color = start_color
        self.end_color = end_color
        self.duration = duration
        self.elapsed = 0.0
        self.current_color = start_color

    def update(self, dt: float):
        """Update transition progress."""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.current_color = self.end_color
            return

        # Linear interpolation
        t = self.elapsed / self.duration
        self.current_color = tuple(
            int(self.start_color[i] + (self.end_color[i] - self.start_color[i]) * t)
            for i in range(3)
        )

    def get_color(self) -> Tuple[int, int, int]:
        """Get current color."""
        return self.current_color

    def reset(self):
        """Reset transition."""
        self.elapsed = 0.0
        self.current_color = self.start_color


class PulseEffect:
    """Pulsing animation effect for colors."""

    def __init__(self, speed: float = 2.0, min_alpha: float = 0.6, max_alpha: float = 1.0):
        self.speed = speed
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.time = 0.0

    def update(self, dt: float):
        """Update pulse animation."""
        self.time += dt * self.speed

    def get_alpha(self) -> float:
        """Get current alpha value."""
        return self.min_alpha + (self.max_alpha - self.min_alpha) * (0.5 + 0.5 * math.sin(self.time))

    def get_color(self, base_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Get pulsed color."""
        alpha = self.get_alpha()
        return tuple(int(c * alpha) for c in base_color)


class WaveEffect:
    """Wave propagation effect."""

    def __init__(self, center: Tuple[int, int] = (0, 0), speed: float = 5.0):
        self.center = center
        self.speed = speed
        self.time = 0.0
        self.wave_radius = 0.0

    def update(self, dt: float):
        """Update wave animation."""
        self.time += dt
        self.wave_radius = self.speed * self.time

    def set_center(self, center: Tuple[int, int]):
        """Set wave center."""
        self.center = center
        self.reset()

    def reset(self):
        """Reset wave animation."""
        self.time = 0.0
        self.wave_radius = 0.0

    def get_intensity(self, position: Tuple[int, int]) -> float:
        """Get wave intensity at position."""
        distance = math.sqrt(
            (position[0] - self.center[0]) ** 2 +
            (position[1] - self.center[1]) ** 2
        )

        if distance > self.wave_radius:
            return 0.0

        # Intensity decreases with distance from wave front
        wave_width = 5.0
        distance_from_front = abs(distance - self.wave_radius)

        if distance_from_front < wave_width:
            return 1.0 - (distance_from_front / wave_width)

        return 0.0
