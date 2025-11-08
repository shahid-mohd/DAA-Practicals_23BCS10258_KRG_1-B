
# After pygame.init()
import ctypes
try:
    # Windows DPI awareness
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
import pygame
import sys
import os

from maze.grid import Grid
from maze.maze_generator import MazeGenerator
from visualization.visualizer import Visualizer
from visualization.algorithm_controller import AlgorithmController
from visualization.ui_manager import UIManager
from visualization.control_panel import ControlPanel
from visualization.status_bar import StatusBar
from utils.constants import *
from utils.file_utils import FileUtils
from utils.export_tools import ExportTools
from config import config
from utils.layout_manager import LayoutManager  # ✅ Added new layout system


class MazeSolver:
    """Main application class for the Maze Solver with dynamic grid resizing."""

    def __init__(self):
        # --- Initialize layout ---
        self.grid_rows = 30
        self.grid_cols = 40
        self.cell_size = 20
        self.layout = LayoutManager(self.grid_rows, self.grid_cols, self.cell_size)

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.layout.window_width, self.layout.window_height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Maze Solver - Pathfinding Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True

        # --- Core Components ---
        self.grid = Grid(self.grid_rows, self.grid_cols)
        self.maze_generator = MazeGenerator(self.grid)
        self.visualizer = Visualizer(self.screen, self.grid, self.layout)
        self.algorithm_controller = AlgorithmController(self.grid)

        # --- UI Components ---
        self.ui_manager = UIManager()
        self.control_panel = ControlPanel(
            self.ui_manager,
            self.algorithm_controller,
            self.maze_generator,
            self.grid,
            self.layout,
            self.resize_grid
        )
        self.status_bar = StatusBar(
            0,
            self.layout.status_bar_y,
            self.layout.window_width,
            self.layout.status_bar_height
        )
        self.control_panel.status_bar_callback = self.status_bar.set_status

        # --- Export Tools ---
        self.export_tools = ExportTools()
        self.recording_frames = False

        # --- Grid Setup ---
        self.selection_mode = None
        self.grid.set_start(1, 1)
        self.grid.set_end(self.grid_rows - 2, self.grid_cols - 2)

        # --- Input State ---
        self.mouse_pressed = False
        self.current_button = 0

    #  GRID & LAYOUT RESIZE
    def resize_grid(self, rows: int, cols: int):
        """Resize the grid and update layout."""
        self.grid_rows = rows
        self.grid_cols = cols
        self.layout.update_grid_size(rows, cols)

        # Save old grid data and positions
        old_grid_data = [[cell.type for cell in row] for row in self.grid.cells]
        old_start = (self.grid.start_cell.row, self.grid.start_cell.col) if self.grid.start_cell else None
        old_end = (self.grid.end_cell.row, self.grid.end_cell.col) if self.grid.end_cell else None

        # Create new grid
        self.grid = Grid(rows, cols)

        # Preserve old cell data if possible
        for r in range(min(len(old_grid_data), rows)):
            for c in range(min(len(old_grid_data[0]), cols)):
                self.grid.cells[r][c].type = old_grid_data[r][c]

        # Reconnect all linked components
        self.maze_generator = MazeGenerator(self.grid)
        self.visualizer.grid = self.grid
        self.visualizer.layout = self.layout
        self.algorithm_controller.grid = self.grid

        # Recreate visualizer with new grid
        self.visualizer = Visualizer(self.screen, self.grid, self.layout)

        # 🔧 FIX: Update control panel's maze_generator reference
        self.control_panel.maze_generator = self.maze_generator
        self.control_panel.grid = self.grid

        # Resize window and reposition elements
        self.screen = pygame.display.set_mode(
            (self.layout.window_width, self.layout.window_height),
            pygame.RESIZABLE
        )
        self.control_panel.update_positions(self.layout)
        self.status_bar.rect.y = self.layout.status_bar_y
        self.status_bar.rect.width = self.layout.window_width

        # Restore or reset start/end positions
        if old_start:
            start_row, start_col = old_start
            if start_row < rows and start_col < cols:
                self.grid.set_start(start_row, start_col)
            else:
                self.grid.set_start(1, 1)
        else:
            self.grid.set_start(1, 1)

        if old_end:
            end_row, end_col = old_end
            if end_row < rows and end_col < cols:
                self.grid.set_end(end_row, end_col)
            else:
                self.grid.set_end(rows - 2, cols - 2)
        else:
            self.grid.set_end(rows - 2, cols - 2)

        # Update status
        self.status_bar.set_status(f"Grid resized to {rows}x{cols}")

    #  EVENT HANDLING
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Let UI handle event first
            if self.ui_manager.handle_event(event):
                continue

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                self.current_button = 0

            elif event.type == pygame.MOUSEMOTION and self.mouse_pressed:
                self._handle_mouse_drag(event)

            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)

    def _handle_mouse_down(self, event):
        if self.algorithm_controller.running:
            return
        """Handle mouse button press."""
        pos = event.pos
        cell_pos = self.layout.get_cell_from_pos(pos[0], pos[1])

        if cell_pos is None:
            return
        row, col = cell_pos

        mods = pygame.key.get_mods()

        # Ctrl + Left Click → set start
        if mods & pygame.KMOD_CTRL and event.button == 1:
            self.grid.set_start(row, col)
            self.status_bar.set_status("Start point moved")
            return

        # Shift + Left Click → set end
        if mods & pygame.KMOD_SHIFT and event.button == 1:
            self.grid.set_end(row, col)
            self.status_bar.set_status("End point moved")
            return

        # Wall drawing mode
        self.mouse_pressed = True
        self.current_button = event.button

        if event.button == 1:  # Left click → draw wall
            if self.grid.cells[row][col].type == 0:
                self.grid.cells[row][col].type = 1
        elif event.button == 3:  # Right click → erase wall
            if self.grid.cells[row][col].type == 1:
                self.grid.cells[row][col].type = 0

    def _handle_mouse_drag(self, event):
        """Handle dragging while drawing walls."""
        if self.algorithm_controller.running:
            return
        pos = event.pos
        cell_pos = self.layout.get_cell_from_pos(pos[0], pos[1])
        if cell_pos is None:
            return

        row, col = cell_pos
        cell = self.grid.cells[row][col]

        if cell == self.grid.start_cell or cell == self.grid.end_cell:
            return

        if self.current_button == 1 and cell.type == 0:
            cell.type = 1
        elif self.current_button == 3 and cell.type == 1:
            cell.type = 0

    # KEYBOARD HANDLING
    def _handle_keypress(self, key: int):
        """Handle keyboard shortcuts."""
        if key == pygame.K_1:
            self.algorithm_controller.set_algorithm("bfs")
            self.control_panel._update_algorithm_highlight()  # 🔧 FIX: Update highlight
            self.status_bar.set_status("Selected: BFS")

        elif key == pygame.K_2:
            self.algorithm_controller.set_algorithm("dijkstra")
            self.control_panel._update_algorithm_highlight()  # 🔧 FIX
            self.status_bar.set_status("Selected: Dijkstra")

        elif key == pygame.K_3:
            self.algorithm_controller.set_algorithm("astar")
            self.control_panel._update_algorithm_highlight()  # 🔧 FIX
            self.status_bar.set_status("Selected: A*")

        elif key == pygame.K_SPACE or key == pygame.K_p:
            if not self.algorithm_controller.running:
                self.algorithm_controller.start()
                self.status_bar.set_status("Algorithm started")
            else:
                self.algorithm_controller.toggle_pause()
                status = "Paused" if self.algorithm_controller.paused else "Resumed"
                self.status_bar.set_status(status)

        elif key == pygame.K_r:
            self.algorithm_controller.reset()
            self.grid.reset_search_states()
            self.status_bar.set_status("Reset")

        elif key == pygame.K_c:
            self.algorithm_controller.reset()
            self.grid.clear_grid()
            self.grid.set_start(1, 1)
            self.grid.set_end(self.grid_rows - 2, self.grid_cols - 2)
            self.status_bar.set_status("Grid cleared")

        elif key == pygame.K_i:
            if not self.algorithm_controller.finished:
                self.algorithm_controller.run_instant()
                self.status_bar.set_status("Algorithm completed instantly")

        # Maze Generation
        elif key == pygame.K_g:
            self.algorithm_controller.reset()
            self.maze_generator.generate_dfs(complexity=0.75)
            self.maze_generator.make_solvable()
            self.grid.set_start(1, 1)
            self.grid.set_end(self.grid_rows - 2, self.grid_cols - 2)
            self.status_bar.set_status("Generated DFS maze")

        elif key == pygame.K_d:
            self.algorithm_controller.reset()
            self.maze_generator.generate_recursive_division(wall_density=0.5)
            self.maze_generator.make_solvable()
            self.grid.set_start(1, 1)
            self.grid.set_end(self.grid_rows - 2, self.grid_cols - 2)
            self.status_bar.set_status("Generated Recursive Division maze")

        elif key == pygame.K_b:
            self.algorithm_controller.reset()
            self.maze_generator.generate_binary_tree()
            self.maze_generator.make_solvable()
            self.grid.set_start(1, 1)
            self.grid.set_end(self.grid_rows - 2, self.grid_cols - 2)
            self.status_bar.set_status("Generated Binary Tree maze")

        elif key == pygame.K_o:
            self.algorithm_controller.reset()
            self.maze_generator.generate_random_obstacles(obstacle_density=0.3)
            self.grid.set_start(1, 1)
            self.grid.set_end(self.grid_rows - 2, self.grid_cols - 2)
            self.status_bar.set_status("Generated random obstacles")

        # Save/Load
        elif key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            filepath = "outputs/saved_maze.txt"
            os.makedirs("outputs", exist_ok=True)
            FileUtils.save_maze_to_text(
                self.grid,
                filepath,
                self.grid.start_cell,
                self.grid.end_cell
            )
            self.status_bar.set_status(f"Saved to {filepath}")

        elif key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
            try:
                maze_data = FileUtils.load_maze_from_text("outputs/saved_maze.txt")
                self.grid = Grid(len(maze_data), len(maze_data[0]))
                FileUtils.apply_maze_data(self.grid, maze_data)
                self.maze_generator = MazeGenerator(self.grid)
                self.visualizer.grid = self.grid
                self.algorithm_controller.grid = self.grid
                self.status_bar.set_status("Maze loaded")
            except Exception as e:
                self.status_bar.set_status(f"Load failed: {e}")

        # Export Tools
        elif key == pygame.K_F12:
            filename = self.export_tools.screenshot(self.screen)
            self.status_bar.set_status(f"Screenshot: {filename}")

        elif key == pygame.K_F11:
            self.recording_frames = not self.recording_frames
            state = "started" if self.recording_frames else "stopped"
            self.status_bar.set_status(f"Recording {state}")

        elif key == pygame.K_F10:
            gif_file = self.export_tools.frames_to_gif()
            if gif_file:
                self.status_bar.set_status(f"GIF saved: {gif_file}")

    #  UPDATE / RENDER
    def update(self):
        """Update game state."""
        dt = self.clock.tick(FPS) / 1000.0

        # Update UI
        self.ui_manager.update(dt)

        # 🔧 FIX: Update status bar timer
        self.status_bar.update(dt)

        # Update animations
        self.visualizer.update_animations(dt)

        # Update algorithm controller
        if self.algorithm_controller.running and not self.algorithm_controller.paused:
            completed = self.algorithm_controller.step()

            if completed:
                stats = self.algorithm_controller.get_stats()
                if stats['path_found']:
                    self.status_bar.set_status(f"Path found! Length: {stats['path_length']}")
                else:
                    self.status_bar.set_status("No path found")

        # Update control panel button states
        self.control_panel.update_button_states()

    def render(self):
        """Render everything."""
        # Clear screen
        self.screen.fill(COLOR_BACKGROUND)

        # Render visualization
        self.visualizer.render()

        # Render UI
        self.ui_manager.render(self.screen)

        # Render status bar with stats
        stats = self.algorithm_controller.get_stats() if self.algorithm_controller.finished else None
        self.status_bar.render(self.screen, stats)

        # Update display
        pygame.display.flip()

        # Record frames if enabled
        if self.recording_frames and self.algorithm_controller.running:
            self.export_tools.create_animation_frames(self.screen)

    #  MAIN LOOP
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    sample_path = "assets/sample_maze.txt"
    if not os.path.exists(sample_path):
        FileUtils.create_sample_maze(sample_path)

    app = MazeSolver()
    app.run()


if __name__ == "__main__":
    main()