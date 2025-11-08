"""Configuration settings for the Maze Solver application."""

import json
import os
from typing import Dict, Any


class Config:
    """Application configuration manager."""

    DEFAULT_CONFIG = {
        'window': {
            'width': 1200,
            'height': 800,
            'fps': 60,
            'title': 'Maze Solver - Pathfinding Visualizer'
        },
        'grid': {
            'rows': 30,
            'cols': 40,
            'cell_size': 20
        },
        'colors': {
            'background': (20, 20, 20),
            'grid_line': (40, 40, 40),
            'wall': (50, 50, 50),
            'empty': (255, 255, 255),
            'start': (0, 255, 0),
            'end': (255, 0, 0),
            'visited': (100, 149, 237),
            'frontier': (147, 112, 219),
            'path': (255, 215, 0),
            'text': (220, 220, 220)
        },
        'algorithms': {
            'default': 'bfs',
            'animation_speed': 20,
            'instant_run': False
        },
        'maze_generation': {
            'default_algorithm': 'dfs',
            'dfs_complexity': 0.75,
            'division_density': 0.5,
            'obstacle_density': 0.3
        },
        'ui': {
            'show_controls': True,
            'show_legend': True,
            'show_stats': True,
            'panel_width': 280
        },
        'performance': {
            'enable_monitoring': False,
            'log_algorithm_stats': True
        },
        'files': {
            'assets_dir': 'assets',
            'outputs_dir': 'outputs',
            'auto_save': False
        }
    }

    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = self.DEFAULT_CONFIG.copy()
                self._deep_update(config, user_config)
                return config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")

        return self.DEFAULT_CONFIG.copy()

    def _deep_update(self, base: dict, update: dict):
        """Recursively update nested dictionaries."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base:
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def save(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, *keys, default=None):
        """Get nested configuration value."""
        value = self.settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys, value):
        """Set nested configuration value."""
        if len(keys) < 1:
            return

        config = self.settings
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.settings = self.DEFAULT_CONFIG.copy()
        self.save()


# Global configuration instance
config = Config()
