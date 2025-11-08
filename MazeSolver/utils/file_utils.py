import os
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np


class FileUtils:
    """Utility class for loading and saving maze files."""

    @staticmethod
    def load_maze_from_text(filepath: str) -> Tuple[
        List[List[int]], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """Load maze from text file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

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
                        row.append(0)
                        start_pos = (row_idx, col_idx)
                    elif char == 'E':
                        row.append(0)
                        end_pos = (row_idx, col_idx)
                    elif char == '1':
                        row.append(1)
                    else:
                        row.append(0)

                grid_data.append(row)

        return grid_data, start_pos, end_pos

    @staticmethod
    def save_maze_to_text(grid: List[List[int]], filepath: str,
                          start_pos: Optional[Tuple[int, int]] = None,
                          end_pos: Optional[Tuple[int, int]] = None):
        """Save maze to text file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as file:
            for row_idx, row in enumerate(grid):
                line = ""
                for col_idx, cell in enumerate(row):
                    if start_pos and (row_idx, col_idx) == start_pos:
                        line += 'S'
                    elif end_pos and (row_idx, col_idx) == end_pos:
                        line += 'E'
                    elif cell == 1:
                        line += '1'
                    else:
                        line += '0'
                file.write(line + '\n')

    @staticmethod
    def load_maze_from_image(filepath: str, threshold: int = 128) -> List[List[int]]:
        """Load maze from image file."""
        img = Image.open(filepath).convert('L')
        img_array = np.array(img)

        grid_data = []
        for row in img_array:
            grid_row = [1 if pixel < threshold else 0 for pixel in row]
            grid_data.append(grid_row)

        return grid_data

    @staticmethod
    def create_sample_maze(filepath: str) -> None:
        """Create a sample maze file."""
        maze_content = """S111111111111111
0000001000000101
0111111111110101
0100000000010001
0101111111011111
0101000001000001
0101011101111101
0001010001000101
1110010111010101
0000010100010001
0111110101111101
0100000101000101
0101111101010101
000100000001000E"""

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            file.write(maze_content)
