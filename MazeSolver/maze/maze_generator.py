import random
from typing import List, Tuple, Optional
from maze.grid import Grid
from utils.constants import CELL_WALL, CELL_EMPTY


class MazeGenerator:
    """Generate random solvable mazes using various algorithms."""

    def __init__(self, grid: Grid):
        self.grid = grid

    def generate_recursive_division(self, wall_density: float = 0.3):
        """
        Generate maze using recursive division algorithm.

        Args:
            wall_density: Probability of creating divisions (0.0-1.0)
        """
        # Clear grid first
        for row in self.grid.cells:
            for cell in row:
                if cell.type not in [CELL_WALL]:
                    cell.type = CELL_EMPTY

        # Add border walls
        self._add_border_walls()

        # Recursive division
        self._divide(1, 1, self.grid.cols - 2, self.grid.rows - 2, wall_density)

    def _divide(self, x: int, y: int, width: int, height: int, density: float):
        """Recursively divide the maze into chambers."""
        if width < 2 or height < 2:
            return

        # Decide whether to divide horizontally or vertically
        horizontal = width < height or (width == height and random.random() < 0.5)

        if horizontal:
            self._divide_horizontally(x, y, width, height, density)
        else:
            self._divide_vertically(x, y, width, height, density)

    def _divide_horizontally(self, x: int, y: int, width: int, height: int, density: float):
        """Create horizontal wall with a gap."""
        if height < 2:
            return

        # Choose wall position
        wall_y = y + random.randint(0, height - 1)

        # Choose gap position
        gap_x = x + random.randint(0, width - 1)

        # Create wall with gap
        for col in range(x, x + width):
            if col != gap_x and random.random() < density:
                self.grid.set_wall(wall_y, col)

        # Recursively divide the two chambers
        self._divide(x, y, width, wall_y - y, density)
        self._divide(x, wall_y + 1, width, y + height - wall_y - 1, density)

    def _divide_vertically(self, x: int, y: int, width: int, height: int, density: float):
        """Create vertical wall with a gap."""
        if width < 2:
            return

        # Choose wall position
        wall_x = x + random.randint(0, width - 1)

        # Choose gap position
        gap_y = y + random.randint(0, height - 1)

        # Create wall with gap
        for row in range(y, y + height):
            if row != gap_y and random.random() < density:
                self.grid.set_wall(row, wall_x)

        # Recursively divide the two chambers
        self._divide(x, y, wall_x - x, height, density)
        self._divide(wall_x + 1, y, x + width - wall_x - 1, height, density)

    def generate_dfs(self, complexity: float = 0.75):
        """
        Generate maze using randomized depth-first search (DFS).
        Creates perfect mazes with high complexity.

        Args:
            complexity: Maze complexity (0.0-1.0)
        """
        # Initialize all cells as walls
        for row in self.grid.cells:
            for cell in row:
                cell.type = CELL_WALL

        # Start from random cell
        start_row = random.randrange(1, self.grid.rows - 1, 2)
        start_col = random.randrange(1, self.grid.cols - 1, 2)

        self.grid.cells[start_row][start_col].type = CELL_EMPTY

        # DFS stack
        stack = [(start_row, start_col)]

        while stack:
            current_row, current_col = stack[-1]

            # Get unvisited neighbors (2 cells away)
            neighbors = []
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

            for dr, dc in directions:
                new_row, new_col = current_row + dr, current_col + dc

                if (0 < new_row < self.grid.rows - 1 and
                        0 < new_col < self.grid.cols - 1 and
                        self.grid.cells[new_row][new_col].type == CELL_WALL):
                    neighbors.append((new_row, new_col, dr, dc))

            if neighbors:
                # Choose random neighbor
                next_row, next_col, dr, dc = random.choice(neighbors)

                # Carve path to neighbor
                wall_row = current_row + dr // 2
                wall_col = current_col + dc // 2

                self.grid.cells[next_row][next_col].type = CELL_EMPTY
                self.grid.cells[wall_row][wall_col].type = CELL_EMPTY

                stack.append((next_row, next_col))
            else:
                stack.pop()

        # Add some random openings based on complexity
        if complexity < 1.0:
            self._add_random_openings(int((1.0 - complexity) * self.grid.rows * self.grid.cols * 0.1))

    def generate_random_obstacles(self, obstacle_density: float = 0.3):
        """
        Generate random obstacles in the grid.

        Args:
            obstacle_density: Percentage of cells that should be walls (0.0-1.0)
        """
        # Clear grid
        for row in self.grid.cells:
            for cell in row:
                cell.type = CELL_EMPTY

        # Add border walls
        self._add_border_walls()

        # Add random obstacles
        for row in range(1, self.grid.rows - 1):
            for col in range(1, self.grid.cols - 1):
                if random.random() < obstacle_density:
                    self.grid.set_wall(row, col)

        # Ensure start and end are clear
        if self.grid.start_cell:
            self.grid.start_cell.type = CELL_EMPTY
        if self.grid.end_cell:
            self.grid.end_cell.type = CELL_EMPTY

    def generate_binary_tree(self):
        """
        Generate maze using binary tree algorithm.
        Creates mazes with a distinct texture.
        """
        # Initialize all cells as empty
        for row in self.grid.cells:
            for cell in row:
                cell.type = CELL_EMPTY

        # Add border walls
        self._add_border_walls()

        # Binary tree algorithm
        for row in range(1, self.grid.rows - 1, 2):
            for col in range(1, self.grid.cols - 1, 2):
                neighbors = []

                # North
                if row > 1:
                    neighbors.append((row - 1, col))

                # East
                if col < self.grid.cols - 2:
                    neighbors.append((row, col + 1))

                if neighbors:
                    wall_row, wall_col = random.choice(neighbors)
                    self.grid.set_wall(wall_row, wall_col)

    def _add_border_walls(self):
        """Add walls around the border of the grid."""
        # Top and bottom borders
        for col in range(self.grid.cols):
            self.grid.set_wall(0, col)
            self.grid.set_wall(self.grid.rows - 1, col)

        # Left and right borders
        for row in range(self.grid.rows):
            self.grid.set_wall(row, 0)
            self.grid.set_wall(row, self.grid.cols - 1)

    def _add_random_openings(self, count: int):
        """Add random openings to make maze less dense."""
        for _ in range(count):
            row = random.randint(1, self.grid.rows - 2)
            col = random.randint(1, self.grid.cols - 2)

            cell = self.grid.get_cell(row, col)
            if cell and cell.type == CELL_WALL:
                cell.type = CELL_EMPTY

    def ensure_solvable(self) -> bool:
        """
        Ensure maze is solvable by checking if path exists.
        Uses simple BFS to verify connectivity.

        Returns:
            True if solvable, False otherwise
        """
        if not self.grid.start_cell or not self.grid.end_cell:
            return False

        from collections import deque

        visited = set()
        queue = deque([self.grid.start_cell])
        visited.add(self.grid.start_cell)

        while queue:
            current = queue.popleft()

            if current == self.grid.end_cell:
                return True

            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False

    def make_solvable(self, max_attempts: int = 10):
        """
        Modify maze to ensure it's solvable.

        Args:
            max_attempts: Maximum number of path-carving attempts
        """
        if self.ensure_solvable():
            return

        # Try to create a path by removing walls
        from collections import deque

        for attempt in range(max_attempts):
            visited = {}
            queue = deque([self.grid.start_cell])
            visited[self.grid.start_cell] = None

            found_path = False

            while queue and not found_path:
                current = queue.popleft()

                if current == self.grid.end_cell:
                    found_path = True
                    break

                # Check all directions including through walls
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_row = current.row + dr
                    new_col = current.col + dc

                    neighbor = self.grid.get_cell(new_row, new_col)

                    if neighbor and neighbor not in visited:
                        visited[neighbor] = current

                        if neighbor.is_empty():
                            queue.append(neighbor)
                        else:
                            # Try breaking through wall
                            if random.random() < 0.3:
                                neighbor.type = CELL_EMPTY
                                queue.append(neighbor)

            if self.ensure_solvable():
                return
