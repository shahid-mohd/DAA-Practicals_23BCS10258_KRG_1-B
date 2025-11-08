import pygame
from typing import List
from visualization.ui_components import UIComponent, Panel, Button, Slider, Label, ToggleButton


class UIManager:
    """Manages all UI components and interactions."""

    def __init__(self):
        self.components: List[UIComponent] = []
        self.panels: List[Panel] = []

    def add_component(self, component: UIComponent):
        """Add a UI component."""
        if isinstance(component, Panel):
            self.panels.append(component)
        self.components.append(component)

    def remove_component(self, component: UIComponent):
        """Remove a UI component."""
        if component in self.components:
            self.components.remove(component)
        if isinstance(component, Panel) and component in self.panels:
            self.panels.remove(component)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame event. Returns True if consumed by UI."""
        for component in reversed(self.components):
            if component.handle_event(event):
                return True
        return False

    def update(self, dt: float):
        """Update all components."""
        for component in self.components:
            component.update(dt)

    def render(self, screen: pygame.Surface):
        """Render all components."""
        for component in self.components:
            component.render(screen)

    def clear(self):
        """Remove all components."""
        self.components.clear()
        self.panels.clear()
