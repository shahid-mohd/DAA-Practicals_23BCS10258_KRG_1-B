import heapq
from typing import List, Tuple, Generator
from maze.grid import Grid, Cell
from utils.timer import Timer


class Dijkstra:
    """Dijkstra's shortest path algorithm."""

    def __init__(self, grid: Grid):
        self.grid = grid
        self.timer = Timer()
        self.nodes_explored = 0
        self.path_length = 0

    def find_path(self) -> Tuple[List[Cell], dict]:
        """
        Find path using Dijkstra's algorithm.

        Returns:
            Tuple of (path, stats)
        """
        if not self.grid.start_cell or not self.grid.end_cell:
            return [], {}

        self.timer.start()
        self.nodes_explored = 0
        self.grid.reset_search_states()

        # Priority queue: (distance, cell)
        pq = [(0, id(self.grid.start_cell), self.grid.start_cell)]
        self.grid.start_cell.distance = 0

        while pq:
            current_dist, _, current = heapq.heappop(pq)

            # Skip if already visited
            if current.visited:
                continue

            current.visited = True
            self.nodes_explored += 1

            # Goal found
            if current == self.grid.end_cell:
                path = self._reconstruct_path(current)
                elapsed = self.timer.stop()
                return path, self._get_stats(elapsed, path)

            # Explore neighbors
            for neighbor in self.grid.get_neighbors(current):
                if not neighbor.visited:
                    new_distance = current.distance + 1  # Uniform cost = 1

                    if new_distance < neighbor.distance:
                        neighbor.distance = new_distance
                        neighbor.parent = current
                        heapq.heappush(pq, (new_distance, id(neighbor), neighbor))

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

        pq = [(0, id(self.grid.start_cell), self.grid.start_cell)]
        self.grid.start_cell.distance = 0

        while pq:
            current_dist, _, current = heapq.heappop(pq)

            if current.visited:
                continue

            current.visited = True
            self.nodes_explored += 1
            yield (current, 'visited')

            # Goal found
            if current == self.grid.end_cell:
                path = self._reconstruct_path(current)

                for cell in path:
                    cell.in_path = True
                    yield (cell, 'path')

                elapsed = self.timer.stop()
                return path, self._get_stats(elapsed, path)

            # Explore neighbors
            for neighbor in self.grid.get_neighbors(current):
                if not neighbor.visited:
                    new_distance = current.distance + 1

                    if new_distance < neighbor.distance:
                        neighbor.distance = new_distance
                        neighbor.parent = current
                        neighbor.in_frontier = True
                        heapq.heappush(pq, (new_distance, id(neighbor), neighbor))
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
            'algorithm': 'Dijkstra',
            'time': elapsed_time,
            'time_formatted': self.timer.format_time(),
            'nodes_explored': self.nodes_explored,
            'path_length': len(path),
            'path_found': len(path) > 0
        }
