from typing import Tuple, Optional, List
from utils.constants import CELL_EMPTY, CELL_WALL, CELL_START, CELL_END

class Cell:
    """Represents a single cell in the maze grid."""

    def __init__(self, row: int, col: int, cell_type: int = CELL_EMPTY):
        self.row = row
        self.col = col
        self.type = cell_type
        self.visited = False
        self.in_frontier = False
        self.in_path = False
        self.distance = float('inf')
        self.parent: Optional['Cell'] = None

    def reset_search_state(self):
        """Reset cell state for new search."""
        self.visited = False
        self.in_frontier = False
        self.in_path = False
        self.distance = float('inf')
        self.parent = None

    def is_wall(self) -> bool:
        """Check if cell is a wall."""
        return self.type == CELL_WALL

    def is_empty(self) -> bool:
        """Check if cell is traversable."""
        return self.type in [CELL_EMPTY, CELL_START, CELL_END]

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f"Cell({self.row}, {self.col})"

class Grid:
    """Represents the entire maze grid."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.cells: List[List[Cell]] = []
        self.start_cell: Optional[Cell] = None
        self.end_cell: Optional[Cell] = None
        self._initialize_grid()

    def _initialize_grid(self):
        """Initialize empty grid."""
        self.cells = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                row_cells.append(Cell(row, col))
            self.cells.append(row_cells)

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get cell at position, return None if out of bounds."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def get_neighbors(self, cell: Cell, include_diagonals: bool = False) -> List[Cell]:
        """Get valid neighboring cells."""
        from utils.constants import DIRECTIONS, DIRECTIONS_8

        directions = DIRECTIONS_8 if include_diagonals else DIRECTIONS
        neighbors = []

        for dr, dc in directions:
            new_row, new_col = cell.row + dr, cell.col + dc
            neighbor = self.get_cell(new_row, new_col)

            if neighbor and neighbor.is_empty():
                neighbors.append(neighbor)

        return neighbors

    def set_start(self, row: int, col: int):
        """Set the start cell."""
        # Validate coordinates
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            row = max(0, min(row, self.rows - 1))
            col = max(0, min(col, self.cols - 1))

        # Clear previous start if exists
        if self.start_cell:
            self.start_cell.type = CELL_EMPTY

        # Set new start
        self.cells[row][col].type = CELL_START
        self.start_cell = self.cells[row][col]

    def set_end(self, row: int, col: int):
        """Set the end cell."""
        # Validate coordinates
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            row = max(0, min(row, self.rows - 1))
            col = max(0, min(col, self.cols - 1))

        # Clear previous end if exists
        if self.end_cell:
            self.end_cell.type = CELL_EMPTY

        # Set new end
        self.cells[row][col].type = CELL_END
        self.end_cell = self.cells[row][col]

    def set_wall(self, row: int, col: int):
        """Set cell as wall."""
        cell = self.get_cell(row, col)
        if cell and cell.type not in [CELL_START, CELL_END]:
            cell.type = CELL_WALL

    def clear_cell(self, row: int, col: int):
        """Clear cell (make it empty)."""
        cell = self.get_cell(row, col)
        if cell and cell.type not in [CELL_START, CELL_END]:
            cell.type = CELL_EMPTY

    def reset_search_states(self):
        """Reset all cells for new search."""
        for row in self.cells:
            for cell in row:
                cell.reset_search_state()

    def clear_grid(self):
        """Clear entire grid."""
        for row in self.cells:
            for cell in row:
                if cell.type not in [CELL_START, CELL_END]:
                    cell.type = CELL_EMPTY
                cell.reset_search_state()

    def load_from_array(self, array: List[List[int]],
                       start_pos: Optional[Tuple[int, int]] = None,
                       end_pos: Optional[Tuple[int, int]] = None):
        """Load grid from 2D array."""
        self.rows = len(array)
        self.cols = len(array[0]) if array else 0
        self._initialize_grid()

        for row_idx, row in enumerate(array):
            for col_idx, cell_type in enumerate(row):
                if cell_type == 1:
                    self.cells[row_idx][col_idx].type = CELL_WALL

        if start_pos:
            self.set_start(start_pos[0], start_pos[1])

        if end_pos:
            self.set_end(end_pos[0], end_pos[1])
