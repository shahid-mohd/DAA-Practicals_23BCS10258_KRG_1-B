import os
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np
from maze.grid import Grid
from utils.constants import CELL_EMPTY, CELL_WALL, CELL_START, CELL_END


class MazeLoader:
    """Load mazes from various file formats."""

    @staticmethod
    def load_from_text(filepath: str) -> Tuple[List[List[int]], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Load maze from text file.

        Format:
        - S = Start
        - E = End
        - 0 = Empty
        - 1 = Wall

        Returns:
            Tuple of (grid_data, start_pos, end_pos)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Maze file not found: {filepath}")

        grid_data = []
        start_pos = None
        end_pos = None

        with open(filepath, 'r') as file:
            for row_idx, line in enumerate(file):
                line = line.strip()
                if not line:
                    continue

                row = []
                for col_idx, char in enumerate(line):
                    if char == 'S':
                        row.append(CELL_EMPTY)
                        start_pos = (row_idx, col_idx)
                    elif char == 'E':
                        row.append(CELL_EMPTY)
                        end_pos = (row_idx, col_idx)
                    elif char == '1':
                        row.append(CELL_WALL)
                    else:
                        row.append(CELL_EMPTY)

                grid_data.append(row)

        return grid_data, start_pos, end_pos

    @staticmethod
    def load_from_image(filepath: str, threshold: int = 128) -> Tuple[
        List[List[int]], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Load maze from image file.
        Dark pixels become walls, light pixels become empty cells.

        Args:
            filepath: Path to image file
            threshold: Brightness threshold (0-255)

        Returns:
            Tuple of (grid_data, start_pos, end_pos)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")

        # Load and convert image to grayscale
        img = Image.open(filepath).convert('L')
        img_array = np.array(img)

        grid_data = []
        for row in img_array:
            grid_row = []
            for pixel in row:
                if pixel < threshold:
                    grid_row.append(CELL_WALL)
                else:
                    grid_row.append(CELL_EMPTY)
            grid_data.append(grid_row)

        # Auto-detect start (top-left empty) and end (bottom-right empty)
        start_pos = MazeLoader._find_empty_cell(grid_data, from_start=True)
        end_pos = MazeLoader._find_empty_cell(grid_data, from_start=False)

        return grid_data, start_pos, end_pos

    @staticmethod
    def _find_empty_cell(grid_data: List[List[int]], from_start: bool = True) -> Optional[Tuple[int, int]]:
        """Find first empty cell from start or end of grid."""
        rows = len(grid_data)
        cols = len(grid_data[0]) if grid_data else 0

        if from_start:
            for row in range(rows):
                for col in range(cols):
                    if grid_data[row][col] == CELL_EMPTY:
                        return (row, col)
        else:
            for row in range(rows - 1, -1, -1):
                for col in range(cols - 1, -1, -1):
                    if grid_data[row][col] == CELL_EMPTY:
                        return (row, col)

        return None

    @staticmethod
    def load_into_grid(grid: Grid, filepath: str, file_type: str = 'auto'):
        """
        Load maze directly into Grid object.

        Args:
            grid: Grid instance to load into
            filepath: Path to maze file
            file_type: 'text', 'image', or 'auto' (detect from extension)
        """
        if file_type == 'auto':
            ext = os.path.splitext(filepath)[1].lower()
            if ext in ['.txt', '.maze']:
                file_type = 'text'
            elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                file_type = 'image'
            else:
                raise ValueError(f"Unknown file type: {ext}")

        if file_type == 'text':
            grid_data, start, end = MazeLoader.load_from_text(filepath)
        elif file_type == 'image':
            grid_data, start, end = MazeLoader.load_from_image(filepath)
        else:
            raise ValueError(f"Invalid file type: {file_type}")

        grid.load_from_array(grid_data, start, end)
