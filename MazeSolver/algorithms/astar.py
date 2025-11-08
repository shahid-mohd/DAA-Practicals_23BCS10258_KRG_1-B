import heapq
from typing import List, Tuple, Generator
from maze.grid import Grid, Cell
from utils.timer import Timer


class AStar:
    """A* pathfinding algorithm with Manhattan distance heuristic."""

    def __init__(self, grid: Grid):
        self.grid = grid
        self.timer = Timer()
        self.nodes_explored = 0
        self.path_length = 0

    def heuristic(self, cell: Cell, goal: Cell) -> float:
        """
        Calculate Manhattan distance heuristic.

        Args:
            cell: Current cell
            goal: Goal cell

        Returns:
            Manhattan distance
        """
        return abs(cell.row - goal.row) + abs(cell.col - goal.col)

    def find_path(self) -> Tuple[List[Cell], dict]:
        """
        Find path using A* algorithm.

        Returns:
            Tuple of (path, stats)
        """
        if not self.grid.start_cell or not self.grid.end_cell:
            return [], {}

        self.timer.start()
        self.nodes_explored = 0
        self.grid.reset_search_states()

        start = self.grid.start_cell
        goal = self.grid.end_cell

        # Priority queue: (f_score, g_score, cell)
        # f_score = g_score + heuristic
        pq = [(self.heuristic(start, goal), 0, id(start), start)]
        start.distance = 0

        # Track g_scores separately
        g_scores = {start: 0}

        while pq:
            _, current_g, _, current = heapq.heappop(pq)

            if current.visited:
                continue

            current.visited = True
            self.nodes_explored += 1

            # Goal found
            if current == goal:
                path = self._reconstruct_path(current)
                elapsed = self.timer.stop()
                return path, self._get_stats(elapsed, path)

            # Explore neighbors
            for neighbor in self.grid.get_neighbors(current):
                if not neighbor.visited:
                    tentative_g = current_g + 1

                    if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                        g_scores[neighbor] = tentative_g
                        neighbor.distance = tentative_g
                        neighbor.parent = current

                        f_score = tentative_g + self.heuristic(neighbor, goal)
                        heapq.heappush(pq, (f_score, tentative_g, id(neighbor), neighbor))

        elapsed = self.timer.stop()
        return [], self._get_stats(elapsed, [])

    def find_path_animated(self) -> Generator[Tuple[Cell, str], None, Tuple[List[Cell], dict]]:
        """
        Find path with step-by-step animation.

        Yields:
            Tuple of (cell, state) where state is 'visiting', 'visited', or 'path'

        Returns:
            Tuple of (path, stats)
        """
        if not self.grid.start_cell or not self.grid.end_cell:
            return [], {}

        self.timer.start()
        self.nodes_explored = 0
        self.grid.reset_search_states()

        start = self.grid.start_cell
        goal = self.grid.end_cell

        pq = [(self.heuristic(start, goal), 0, id(start), start)]
        start.distance = 0
        g_scores = {start: 0}

        while pq:
            _, current_g, _, current = heapq.heappop(pq)

            if current.visited:
                continue

            current.visited = True
            self.nodes_explored += 1
            yield (current, 'visited')

            # Goal found
            if current == goal:
                path = self._reconstruct_path(current)

                for cell in path:
                    cell.in_path = True
                    yield (cell, 'path')

                elapsed = self.timer.stop()
                return path, self._get_stats(elapsed, path)

            # Explore neighbors
            for neighbor in self.grid.get_neighbors(current):
                if not neighbor.visited:
                    tentative_g = current_g + 1

                    if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                        g_scores[neighbor] = tentative_g
                        neighbor.distance = tentative_g
                        neighbor.parent = current
                        neighbor.in_frontier = True

                        f_score = tentative_g + self.heuristic(neighbor, goal)
                        heapq.heappush(pq, (f_score, tentative_g, id(neighbor), neighbor))
                        yield (neighbor, 'frontier')

        elapsed = self.timer.stop()
        return [], self._get_stats(elapsed, [])

    def _reconstruct_path(self, end_cell: Cell) -> List[Cell]:
        """Reconstruct path from end to start."""
        path = []
        current = end_cell

        while current:
            path.append(current)
            current = current.parent

        path.reverse()
        self.path_length = len(path)
        return path

    def _get_stats(self, elapsed_time: float, path: List[Cell]) -> dict:
        """Get algorithm statistics."""
        return {
            'algorithm': 'A*',
            'time': elapsed_time,
            'time_formatted': self.timer.format_time(),
            'nodes_explored': self.nodes_explored,
            'path_length': len(path),
            'path_found': len(path) > 0
        }
