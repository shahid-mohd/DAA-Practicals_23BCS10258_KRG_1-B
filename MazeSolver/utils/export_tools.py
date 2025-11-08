import pygame
import os
from datetime import datetime
from typing import Optional, Tuple
from PIL import Image
import numpy as np


class ExportTools:
    """Tools for exporting mazes and visualizations."""

    @staticmethod
    def screenshot(screen: pygame.Surface, filename: Optional[str] = None) -> str:
        """Take screenshot of current screen."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"outputs/screenshot_{timestamp}.png"

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pygame.image.save(screen, filename)
        return filename

    @staticmethod
    def export_maze_as_image(grid, filename: str, cell_size: int = 20):
        """Export maze as image file."""
        from maze.grid import Grid

        width = grid.cols * cell_size
        height = grid.rows * cell_size

        # Create image
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        pixels = img.load()

        for row in grid.cells:
            for cell in row:
                x_start = cell.col * cell_size
                y_start = cell.row * cell_size

                # Determine color
                if cell.type == 1:  # Wall
                    color = (0, 0, 0)
                elif cell.type == 2:  # Start
                    color = (0, 255, 0)
                elif cell.type == 3:  # End
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 255)

                # Fill cell
                for dx in range(cell_size):
                    for dy in range(cell_size):
                        if x_start + dx < width and y_start + dy < height:
                            pixels[x_start + dx, y_start + dy] = color

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img.save(filename)
        return filename

    @staticmethod
    def create_animation_frames(screen: pygame.Surface, frame_dir: str = "outputs/frames"):
        """Save animation frame."""
        os.makedirs(frame_dir, exist_ok=True)

        # Count existing frames
        existing_frames = len([f for f in os.listdir(frame_dir) if f.endswith('.png')])
        filename = os.path.join(frame_dir, f"frame_{existing_frames:04d}.png")

        pygame.image.save(screen, filename)
        return filename

    @staticmethod
    def frames_to_gif(frame_dir: str = "outputs/frames", output_file: str = "outputs/animation.gif", duration: int = 50):
        """Convert animation frames to GIF."""
        try:
            from PIL import Image
            import glob

            frames = []
            frame_files = sorted(glob.glob(os.path.join(frame_dir, "frame_*.png")))

            for frame_file in frame_files:
                frames.append(Image.open(frame_file))

            if frames:
                frames[0].save(
                    output_file,
                    save_all=True,
                    append_images=frames[1:],
                    duration=duration,
                    loop=0
                )
                print(f"Created GIF: {output_file}")
                return output_file
        except Exception as e:
            print(f"Error creating GIF: {e}")

        return None
