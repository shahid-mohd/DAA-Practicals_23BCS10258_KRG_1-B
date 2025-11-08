"""Test script for pathfinding algorithms."""

from maze.grid import Grid
from algorithms import BFS, Dijkstra, AStar


def create_simple_maze():
    """Create a simple test maze."""
    grid = Grid(10, 10)

    # Add some walls
    for i in range(3, 8):
        grid.set_wall(i, 5)

    # Set start and end
    grid.set_start(0, 0)
    grid.set_end(9, 9)

    return grid


def test_algorithm(algorithm_class, grid):
    """Test a single algorithm."""
    print(f"\nTesting {algorithm_class.__name__}:")
    print("-" * 50)

    algorithm = algorithm_class(grid)
    path, stats = algorithm.find_path()

    print(f"Algorithm: {stats['algorithm']}")
    print(f"Path Found: {stats['path_found']}")
    print(f"Path Length: {stats['path_length']}")
    print(f"Nodes Explored: {stats['nodes_explored']}")
    print(f"Time: {stats['time_formatted']}")


def main():
    """Run algorithm tests."""
    grid = create_simple_maze()

    test_algorithm(BFS, grid)
    grid.reset_search_states()

    test_algorithm(Dijkstra, grid)
    grid.reset_search_states()

    test_algorithm(AStar, grid)


if __name__ == "__main__":
    main()
