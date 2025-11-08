import pygame
from typing import Callable, Optional, Tuple
from utils.constants import COLOR_TEXT, COLOR_BACKGROUND, COLOR_START, COLOR_END
from utils.fonts import FontManager

class UIComponent:
    """Base class for UI components."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame event. Returns True if event was consumed."""
        return False

    def update(self, dt: float):
        """Update component state."""
        pass

    def render(self, screen: pygame.Surface):
        """Render the component."""
        pass


class Button(UIComponent):
    """Interactive button with hover and click effects."""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, callback: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.pressed = False

        # Colors (now public so they can be modified)
        self.color_normal = (70, 70, 70)
        self.color_hover = (90, 90, 90)
        self.color_pressed = (50, 50, 50)
        self.color_disabled = (40, 40, 40)
        self.text_color = COLOR_TEXT
        self.text_color_disabled = (100, 100, 100)

        # Font
        self.font = pygame.font.Font(None, 24)


    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                if self.rect.collidepoint(event.pos) and self.callback:
                    self.callback()
                return True

        return False

    def render(self, screen: pygame.Surface):
        if not self.visible:
            return

        # Determine color
        if not self.enabled:
            color = self.color_disabled
            text_color = self.text_color_disabled
        elif self.pressed:
            color = self.color_pressed
            text_color = self.text_color
        elif self.hovered:
            color = self.color_hover
            text_color = self.text_color
        else:
            color = self.color_normal
            text_color = self.text_color

        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Slider(UIComponent):
    """Horizontal slider for adjusting values."""

    def __init__(self, x: int, y: int, width: int, height: int,
                 min_value: float, max_value: float, initial_value: float,
                 label: str = "", callback: Optional[Callable[[float], None]] = None):
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        self.callback = callback

        self.dragging = False
        self.handle_radius = height // 2

        # Colors
        self.track_color = (60, 60, 60)
        self.handle_color = COLOR_START
        self.handle_color_hover = COLOR_END

        # Font
        self.font = pygame.font.Font(None, 20)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_x = self._get_handle_x()
                handle_rect = pygame.Rect(
                    handle_x - self.handle_radius,
                    self.rect.y,
                    self.handle_radius * 2,
                    self.rect.height
                )
                if handle_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self._update_value_from_pos(event.pos[0])
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value_from_pos(event.pos[0])
                return True

        return False

    def _get_handle_x(self) -> int:
        """Get X position of slider handle."""
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        return int(self.rect.x + ratio * self.rect.width)

    def _update_value_from_pos(self, x: int):
        """Update value based on mouse X position."""
        ratio = (x - self.rect.x) / self.rect.width
        ratio = max(0.0, min(1.0, ratio))
        old_value = self.value
        self.value = self.min_value + ratio * (self.max_value - self.min_value)

        # Only call callback if value changed significantly
        if abs(old_value - self.value) > 0.5:
            if self.callback:
                self.callback(self.value)

    def set_value(self, value: float):
        """Set slider value programmatically."""
        self.value = max(self.min_value, min(self.max_value, value))

    def render(self, screen: pygame.Surface):
        if not self.visible:
            return

        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, COLOR_TEXT)
            screen.blit(label_surface, (self.rect.x, self.rect.y - 20))

        # Draw track
        pygame.draw.rect(screen, self.track_color, self.rect)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 1)

        # Draw handle
        handle_x = self._get_handle_x()
        handle_color = self.handle_color_hover if self.dragging else self.handle_color
        pygame.draw.circle(screen, handle_color, (handle_x, self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, COLOR_TEXT, (handle_x, self.rect.centery), self.handle_radius, 2)

        # Draw value
        value_text = f"{int(self.value)}"
        value_surface = self.font.render(value_text, True, COLOR_TEXT)
        screen.blit(value_surface, (self.rect.right + 10, self.rect.y))


class Label(UIComponent):
    """Text label component."""

    def __init__(self, x: int, y: int, text: str, font_size: int = 24, color: Tuple[int, int, int] = None):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.color = color or COLOR_TEXT
        self.font = pygame.font.Font(None, font_size)
        self._update_size()

    def set_text(self, text: str):
        """Update label text."""
        self.text = text
        self._update_size()

    def _update_size(self):
        """Update component size based on text."""
        surface = self.font.render(self.text, True, self.color)
        self.rect.width = surface.get_width()
        self.rect.height = surface.get_height()

    def render(self, screen: pygame.Surface):
        if not self.visible:
            return

        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect.topleft)


class Panel(UIComponent):
    """Container panel for grouping UI components."""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        super().__init__(x, y, width, height)
        self.title = title
        self.components = []
        self.background_color = (30, 30, 30)
        self.border_color = COLOR_TEXT
        self.title_font = pygame.font.Font(None, 28)

    def add_component(self, component: UIComponent):
        """Add a component to the panel."""
        self.components.append(component)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        for component in self.components:
            if component.handle_event(event):
                return True

        return False

    def update(self, dt: float):
        for component in self.components:
            component.update(dt)

    def render(self, screen: pygame.Surface):
        if not self.visible:
            return

        # Draw background
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        # Draw title
        if self.title:
            title_surface = self.title_font.render(self.title, True, COLOR_TEXT)
            title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 10)
            screen.blit(title_surface, title_rect)

        # Draw components
        for component in self.components:
            component.render(screen)


class ToggleButton(Button):
    """Toggle button that stays in pressed/unpressed state."""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, callback: Optional[Callable[[bool], None]] = None):
        super().__init__(x, y, width, height, text, None)
        self.toggled = False
        self.toggle_callback = callback

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.toggled = not self.toggled
                if self.toggle_callback:
                    self.toggle_callback(self.toggled)
                return True

        return False

    def render(self, screen: pygame.Surface):
        if not self.visible:
            return

        # Determine color
        if not self.enabled:
            color = self.color_disabled
            text_color = self.text_color_disabled
        elif self.toggled:
            color = self.color_pressed
            text_color = self.text_color
        elif self.hovered:
            color = self.color_hover
            text_color = self.text_color
        else:
            color = self.color_normal
            text_color = self.text_color

        # Draw button
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
