"""Controls algorithm execution and state."""

from typing import Optional, Dict, List, Tuple, Any
from algorithms import AlgorithmFactory
from maze.grid import Grid
from utils.timer import Timer


class AlgorithmController:
    """Manages algorithm execution and state."""

    def __init__(self, grid: Grid):
        self.grid = grid
        self.algorithm_name = "bfs"
        self.algorithm = None
        self.running = False
        self.paused = False
        self.finished = False
        self.speed = 20  # Steps per second
        self.steps_per_frame = 1

        # Results
        self.path = None
        self.stats = {
            'time_taken': 0.0,
            'nodes_explored': 0,
            'path_length': 0,
            'path_found': False,
            'algorithm_name': ''
        }

        # Timer
        self.timer = Timer()

        # State
        self.generator = None
        self.last_step_time = 0.0
        self.step_delay = 1.0 / self.speed

    def set_algorithm(self, algorithm_name: str):
        """Set the current algorithm."""
        self.algorithm_name = algorithm_name
        self.reset()

    def set_speed(self, speed: int):
        """Set visualization speed (steps per second)."""
        self.speed = max(1, min(100, speed))
        self.step_delay = 1.0 / self.speed
        self.steps_per_frame = max(1, self.speed // 20)

    def start(self):
        """Start algorithm execution."""
        if self.finished:
            self.reset()

        self.running = True
        self.paused = False
        self.finished = False

        # Create algorithm instance
        self.algorithm = AlgorithmFactory.create(
            self.algorithm_name,
            self.grid
        )

        # Get generator for step-by-step execution
        self.generator = self.algorithm.find_path_animated()

        # Start timer
        self.timer.start()

    def step(self) -> bool:
        """Execute one step of the algorithm. Returns True if completed."""
        if not self.running or self.paused or self.finished or not self.generator:
            return False

        try:
            # Execute multiple steps based on speed
            for _ in range(self.steps_per_frame):
                next(self.generator)

        except StopIteration as e:
            # Algorithm completed
            self.finish(e.value if hasattr(e, 'value') else None)
            return True

        return False

    def finish(self, result: Optional[Tuple[List, Dict]] = None):
        """Finish algorithm execution."""
        self.running = False
        self.finished = True

        # Stop timer
        elapsed_time = self.timer.stop()

        # Process results
        if result:
            path, algorithm_stats = result
            self.path = path

            # Update stats
            self.stats = {
                'time_taken': elapsed_time,
                'nodes_explored': algorithm_stats.get('nodes_explored', 0),
                'path_length': len(path) if path else 0,
                'path_found': bool(path),
                'algorithm_name': self.algorithm_name.upper()
            }

            # Mark path cells
            if path:
                for cell in path:
                    cell.in_path = True
        else:
            # No result (shouldn't happen normally)
            self.stats = {
                'time_taken': elapsed_time,
                'nodes_explored': 0,
                'path_length': 0,
                'path_found': False,
                'algorithm_name': self.algorithm_name.upper()
            }

    def toggle_pause(self):
        """Pause or resume algorithm execution."""
        if self.running:
            self.paused = not self.paused

    def reset(self):
        """Reset algorithm state."""
        self.running = False
        self.paused = False
        self.finished = False
        self.path = None
        self.generator = None

        # Reset stats
        self.stats = {
            'time_taken': 0.0,
            'nodes_explored': 0,
            'path_length': 0,
            'path_found': False,
            'algorithm_name': self.algorithm_name.upper()
        }

        # Reset timer
        self.timer.reset()

    def run_instant(self) -> Tuple[Optional[List], Dict]:
        """Run algorithm instantly without animation."""
        self.reset()
        self.running = True

        # Create algorithm
        self.algorithm = AlgorithmFactory.create(
            self.algorithm_name,
            self.grid
        )

        # Start timer
        self.timer.start()

        # Run algorithm - Fixed: use self.algorithm instead of algorithm
        path, algorithm_stats = self.algorithm.find_path()

        # Stop timer
        elapsed_time = self.timer.stop()

        # Update stats
        self.stats = {
            'time_taken': elapsed_time,
            'nodes_explored': algorithm_stats.get('nodes_explored', 0),
            'path_length': len(path) if path else 0,
            'path_found': bool(path),
            'algorithm_name': self.algorithm_name.upper()
        }

        # Mark path
        if path:
            for cell in path:
                cell.in_path = True

        self.path = path
        self.finished = True
        self.running = False

        return path, self.stats

    def get_stats(self) -> Dict[str, Any]:
        """Get current algorithm statistics."""
        return self.stats.copy()

    def get_status_text(self) -> str:
        """Get status text for display."""
        if not self.running and not self.finished:
            return f"Ready - {self.algorithm_name.upper()}"

        if self.paused:
            return "Paused"

        if self.running:
            return f"Running {self.algorithm_name.upper()}..."

        if self.finished:
            if self.stats['path_found']:
                return f"Complete - Path Found ({self.stats['path_length']} steps)"
            else:
                return "Complete - No Path Found"

        return ""
