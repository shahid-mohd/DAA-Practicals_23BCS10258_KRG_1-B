# visualization/control_panel.py
import pygame
from visualization.ui_components import Panel, Button, Slider, Label
from utils.constants import *


class ControlPanel:
    """Main control panel for the application."""

    def __init__(self, ui_manager, algorithm_controller, maze_generator,
                 grid, layout, resize_callback):
        self.ui_manager = ui_manager
        self.algorithm_controller = algorithm_controller
        self.maze_generator = maze_generator
        self.grid = grid
        self.layout = layout
        self.resize_callback = resize_callback

        self.main_panel = None
        self.pending_rows = grid.rows
        self.pending_cols = grid.cols

        self._create_panel()

    def _create_panel(self):
        """Create the control panel with all components."""
        # Remove old panel
        if self.main_panel:
            self.ui_manager.remove_component(self.main_panel)

        # Create main panel
        self.main_panel = Panel(
            self.layout.panel_x,
            self.layout.panel_y,
            self.layout.panel_width,
            min(self.layout.panel_height, 650),
            "Controls"
        )

        y_offset = 50
        button_width = self.layout.panel_width - 40
        half_button_width = (button_width - 10) // 2
        button_height = 35
        button_x = self.layout.panel_x + 20

        # === GRID SIZE SECTION ===
        self._add_section_header("Grid Size", button_x, y_offset)
        y_offset += 40

        # Rows slider
        self.rows_slider = Slider(
            button_x, self.layout.panel_y + y_offset,
                      button_width - 50, 15,
            10, 30, min(self.pending_rows, 30),
            "Rows:",
            self._on_rows_change
        )
        self.main_panel.add_component(self.rows_slider)
        y_offset += 40

        # Cols slider
        self.cols_slider = Slider(
            button_x, self.layout.panel_y + y_offset,
                      button_width - 50, 15,
            10, 50, min(self.pending_cols, 50),
            "Cols:",
            self._on_cols_change
        )
        self.main_panel.add_component(self.cols_slider)
        y_offset += 30

        # Apply button
        self.apply_size_button = Button(
            button_x, self.layout.panel_y + y_offset,
            button_width, button_height,
            "Apply Size",
            self._apply_grid_size
        )
        self.main_panel.add_component(self.apply_size_button)
        y_offset += button_height + 20

        # === ALGORITHM SECTION ===
        self._add_section_header("Algorithm", button_x, y_offset)
        y_offset += 20

        algorithms = [
            ("BFS", "bfs"),
            ("Dijkstra", "dijkstra"),
            ("A*", "astar")
        ]

        # Store algorithm buttons for highlighting
        self.algorithm_buttons = {}

        for name, algo_id in algorithms:
            btn = Button(
                button_x, self.layout.panel_y + y_offset,
                button_width, button_height,
                name,
                lambda a=algo_id: self._select_algorithm(a)
            )
            self.algorithm_buttons[algo_id] = btn
            self.main_panel.add_component(btn)
            y_offset += button_height + 8

        y_offset += 10

        # === EXECUTION SECTION ===
        self._add_section_header("Execution", button_x, y_offset)
        y_offset += 20

        # Start and Reset buttons side by side
        self.start_button = Button(
            button_x, self.layout.panel_y + y_offset,
            half_button_width, button_height,
            "Start",
            self._toggle_algorithm
        )
        self.main_panel.add_component(self.start_button)

        self.reset_button = Button(
            button_x + half_button_width + 10, self.layout.panel_y + y_offset,
            half_button_width, button_height,
            "Reset",
            self._reset
        )
        self.main_panel.add_component(self.reset_button)
        y_offset += button_height + 25

        # === SPEED SECTION ===
        self._add_section_header("Speed", button_x, y_offset)
        y_offset += 30

        self.speed_slider = Slider(
            button_x, self.layout.panel_y + y_offset,
                      button_width - 50, 15,
            1, 100, self.algorithm_controller.speed,
            "",
            self._on_speed_change
        )
        self.main_panel.add_component(self.speed_slider)
        y_offset += 45

        # === MAZE GENERATION SECTION ===
        self._add_section_header("Maze Generation", button_x, y_offset)
        y_offset += 30

        # First row: DFS and Recursive Division
        btn1 = Button(
            button_x, self.layout.panel_y + y_offset,
            half_button_width, button_height,
            "DFS Maze",
            self._generate_dfs_maze
        )
        self.main_panel.add_component(btn1)

        btn2 = Button(
            button_x + half_button_width + 10, self.layout.panel_y + y_offset,
            half_button_width, button_height,
            "Recursive Div",
            self._generate_division_maze
        )
        self.main_panel.add_component(btn2)
        y_offset += button_height + 8

        # Second row: Random Obstacles and Clear Grid
        btn3 = Button(
            button_x, self.layout.panel_y + y_offset,
            half_button_width, button_height,
            "Obstacles",
            self._generate_obstacles
        )
        self.main_panel.add_component(btn3)

        btn4 = Button(
            button_x + half_button_width + 10, self.layout.panel_y + y_offset,
            half_button_width, button_height,
            "Clear Grid",
            self._clear_grid
        )
        self.main_panel.add_component(btn4)

        self.ui_manager.add_component(self.main_panel)

        # Highlight current algorithm
        self._update_algorithm_highlight()

    def _select_algorithm(self, algo_id: str):
        """Select algorithm and update UI."""
        self.selected_algorithm = algo_id
        self.algorithm_controller.set_algorithm(algo_id)
        self._update_algorithm_highlight()

        # Use the status bar callback if available
        if self.status_bar_callback:
            algo_name = algo_id.upper()
            self.status_bar_callback(f"Selected: {algo_name}")

    def _update_algorithm_highlight(self):
        """Update visual highlight for selected algorithm."""
        current_algo = self.algorithm_controller.algorithm_name

        for algo_id, button in self.algorithm_buttons.items():
            if algo_id == current_algo:
                # Highlight active algorithm
                button.color_normal = (60, 120, 180)
                button.color_hover = (80, 140, 200)
            else:
                # Reset to default colors
                button.color_normal = (70, 70, 70)
                button.color_hover = (90, 90, 90)

    def _add_section_header(self, text: str, x: int, y_offset: int):
        """Add a section header label."""
        label = Label(x, self.layout.panel_y + y_offset, text, 24)
        self.main_panel.add_component(label)

    def update_positions(self, layout):
        """Update panel positions after layout change."""
        self.layout = layout
        self._create_panel()

    def _on_rows_change(self, value: float):
        """Handle rows slider change."""
        self.pending_rows = int(value)

    def _on_cols_change(self, value: float):
        """Handle cols slider change."""
        self.pending_cols = int(value)

    def _apply_grid_size(self):
        """Apply new grid size."""
        new_rows = min(int(self.pending_rows), 30)
        new_cols = min(int(self.pending_cols), 50)
        self._reset()
        self.resize_callback(new_rows, new_cols)
        self.rows_slider.set_value(new_rows)
        self.cols_slider.set_value(new_cols)
        # 🔧 FIX: Changed 'cols' to 'new_cols'
        if hasattr(self, 'status_bar_callback'):
            self.status_bar_callback(f"Grid resized to {new_rows}x{new_cols}")

    def _toggle_algorithm(self):
        """Start or pause algorithm."""
        if not self.algorithm_controller.running:
            if self.algorithm_controller.finished:
                self._reset()
            self.algorithm_controller.start()
            self.start_button.text = "Pause"
            # 🔧 FIX: Add status message
            if hasattr(self, 'status_bar_callback'):
                self.status_bar_callback("Algorithm started")
        else:
            self.algorithm_controller.toggle_pause()
            if self.algorithm_controller.paused:
                self.start_button.text = "Resume"
                if hasattr(self, 'status_bar_callback'):
                    self.status_bar_callback("Paused")
            else:
                self.start_button.text = "Pause"
                if hasattr(self, 'status_bar_callback'):
                    self.status_bar_callback("Resumed")

    def _reset(self):
        """Reset algorithm and search states."""
        self.algorithm_controller.reset()
        self.grid.reset_search_states()
        self.start_button.text = "Start"
        # 🔧 FIX: Add status message
        if hasattr(self, 'status_bar_callback'):
            self.status_bar_callback("Reset")

    def _on_speed_change(self, value: float):
        """Handle speed slider change."""
        self.algorithm_controller.set_speed(int(value))

    def _generate_dfs_maze(self):
        """Generate DFS maze."""
        self._reset()
        self.maze_generator.generate_dfs(complexity=0.75)
        self.maze_generator.make_solvable()
        self._set_default_start_end()
        # 🔧 FIX: Add status message
        if hasattr(self, 'status_bar_callback'):
            self.status_bar_callback("Generated DFS maze")

    def _generate_division_maze(self):
        """Generate recursive division maze."""
        self._reset()
        self.maze_generator.generate_recursive_division(wall_density=0.5)
        self.maze_generator.make_solvable()
        self._set_default_start_end()
        # 🔧 FIX: Add status message
        if hasattr(self, 'status_bar_callback'):
            self.status_bar_callback("Generated Recursive Division maze")

    def _generate_obstacles(self):
        """Generate random obstacles."""
        self._reset()
        self.maze_generator.generate_random_obstacles(obstacle_density=0.3)
        self._set_default_start_end()
        # 🔧 FIX: Add status message
        if hasattr(self, 'status_bar_callback'):
            self.status_bar_callback("Generated random obstacles")

    def _clear_grid(self):
        """Clear the grid."""
        self._reset()
        self.grid.clear_grid()
        self._set_default_start_end()
        # 🔧 FIX: Add status message
        if hasattr(self, 'status_bar_callback'):
            self.status_bar_callback("Grid cleared")

    def _set_default_start_end(self):
        """Set default start and end positions."""
        self.grid.set_start(1, 1)
        self.grid.set_end(self.grid.rows - 2, self.grid.cols - 2)

    def update_button_states(self):
        """Update button states based on algorithm state."""
        if self.algorithm_controller.running:
            if self.algorithm_controller.paused:
                self.start_button.text = "Resume"
            else:
                self.start_button.text = "Pause"
        else:
            self.start_button.text = "Start"
