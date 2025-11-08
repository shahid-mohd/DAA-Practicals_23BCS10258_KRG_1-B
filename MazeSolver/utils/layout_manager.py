"""Manages dynamic layout based on grid and window size."""


class LayoutManager:
    """Calculate and manage layout dimensions."""

    def __init__(self, grid_rows: int, grid_cols: int, cell_size: int = 20):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size

        # Margins and spacing
        self.top_margin = 40
        self.bottom_margin = 60
        self.left_margin = 40
        self.right_margin = 340  # Space for control panel
        self.panel_width = 300
        self.panel_margin = 20

        self._calculate_layout()

    def _calculate_layout(self):
        """Calculate all layout dimensions."""
        # Grid dimensions
        self.grid_width = self.grid_cols * self.cell_size
        self.grid_height = self.grid_rows * self.cell_size

        # Grid position
        self.grid_x = self.left_margin
        self.grid_y = self.top_margin

        # Window dimensions
        self.window_width = self.left_margin + self.grid_width + self.right_margin
        self.window_height = max(
            self.top_margin + self.grid_height + self.bottom_margin,
            800  # Minimum height
        )

        # Control panel position
        self.panel_x = self.grid_x + self.grid_width + self.panel_margin
        self.panel_y = self.grid_y
        self.panel_height = min(650, self.window_height - self.panel_y - 60)

        # Status bar position
        self.status_bar_y = self.window_height - 110
        self.status_bar_height = 50

    def update_grid_size(self, rows: int, cols: int, cell_size: int = None):
        """Update grid size and recalculate layout."""
        self.grid_rows = rows
        self.grid_cols = cols
        if cell_size:
            self.cell_size = cell_size
        self._calculate_layout()

    def get_cell_from_pos(self, x: int, y: int):
        """Convert screen coordinates to grid cell coordinates."""
        if (self.grid_x <= x < self.grid_x + self.grid_width and
            self.grid_y <= y < self.grid_y + self.grid_height):

            col = (x - self.grid_x) // self.cell_size
            row = (y - self.grid_y) // self.cell_size

            if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
                return (row, col)
        return None

    def get_cell_rect(self, row: int, col: int):
        """Get screen rectangle for a cell."""
        x = self.grid_x + col * self.cell_size
        y = self.grid_y + row * self.cell_size
        return (x, y, self.cell_size, self.cell_size)
