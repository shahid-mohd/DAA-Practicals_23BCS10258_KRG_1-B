from typing import Optional
from maze.grid import Grid
from algorithms.bfs import BFS
from algorithms.dijkstra import Dijkstra
from algorithms.astar import AStar


class AlgorithmFactory:
    """Factory for creating pathfinding algorithm instances."""

    ALGORITHMS = {
        'bfs': BFS,
        'dijkstra': Dijkstra,
        'astar': AStar,
        'a*': AStar
    }

    @staticmethod
    def create(algorithm_name: str, grid: Grid):
        """
        Create algorithm instance.

        Args:
            algorithm_name: Name of algorithm ('bfs', 'dijkstra', 'astar')
            grid: Grid instance

        Returns:
            Algorithm instance

        Raises:
            ValueError: If algorithm name is invalid
        """
        algorithm_name = algorithm_name.lower()

        if algorithm_name not in AlgorithmFactory.ALGORITHMS:
            available = ', '.join(AlgorithmFactory.ALGORITHMS.keys())
            raise ValueError(f"Unknown algorithm: {algorithm_name}. Available: {available}")

        algorithm_class = AlgorithmFactory.ALGORITHMS[algorithm_name]
        return algorithm_class(grid)

    @staticmethod
    def get_available_algorithms() -> list:
        """Get list of available algorithm names."""
        return list(set(AlgorithmFactory.ALGORITHMS.keys()))
