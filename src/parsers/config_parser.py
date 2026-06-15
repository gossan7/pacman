import json
from typing import Any

_CONFIG_CONTENT = {
    "fps": int,
    "seed": int,
    "width": int,
    "length": int,
    "height": int,
    "lives": int,
    "gum_val": int,
    "supergum_val": int,
    "ghost_val": int,
    "level_max_time": int,
    "frightened_duration": float,
    "pacman_speed": int,
    "ghost_speed": int,
    "num_levels": int,
    "highscore_filename": str
}

_DEFAULT_CONFIG = {
    "fps": 60,
    "seed": 42,
    "width": 10,
    "length": 10,
    "height": 10,
    "lives": 3,
    "gum_val": 10,
    "supergum_val": 50,
    "ghost_val": 200,
    "level_max_time": 90,
    "frightened_duration": 7.0,
    "pacman_speed": 10,
    "ghost_speed": 6,
    "num_levels": 1,
    "highscore_filename": "highSCORE.json"
}


class ConfigParser:

    def parse(self, filename: str) -> dict[str, Any]:
        res: dict[str, Any] = {}

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file '{filename}' not found. "
                  f"Using default config.")
            return _DEFAULT_CONFIG.copy()
        except json.JSONDecodeError as e:
            print(f"Warning: Config file '{filename}' is not valid JSON: {e}. "
                  f"Using default config.")
            return _DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Warning: Could not read config file '{filename}': {e}. "
                  f"Using default config.")
            return _DEFAULT_CONFIG.copy()

        if not isinstance(content, dict):
            print("Warning: Config must be a JSON object (dict). "
                  "Using default config.")
            return _DEFAULT_CONFIG.copy()

        for key, value in content.items():

            if key not in _CONFIG_CONTENT:
                raise ValueError(f"Key '{key}' is not a valid argument")

            if not isinstance(value, _CONFIG_CONTENT[key]):
                raise ValueError(
                    f"Key '{key}' must be {_CONFIG_CONTENT[key].__name__}, "
                    f"got {type(value).__name__}"
                )

            if key in res:
                raise ValueError(f"Key '{key}' is set more than once")

            if key == "fps":
                if not 30 <= value <= 60:
                    raise ValueError("FPS must be between 30 and 60")

            elif key in ["width", "length"]:
                if value < 10:
                    raise ValueError(
                        f"{key.capitalize()} must be at least 10")

            elif key == "height":
                if value < 10:
                    raise ValueError("Height must be at least 10")

            elif key == "lives":
                if value <= 0:
                    raise ValueError("Must have at least 1 life")

            elif key == "level_max_time":
                if value <= 0:
                    raise ValueError("Max level time must be greater than 0")

            elif key == "frightened_duration":
                if value <= 0.0:
                    raise ValueError(
                        "Frightened duration must be greater than 0")

            elif key in ["pacman_speed", "ghost_speed"]:
                if value <= 0:
                    raise ValueError(
                        f"{key} must be greater than 0")

            elif key == "num_levels":
                if value <= 0:
                    raise ValueError("Must have at least 1 level")

            elif key == "highscore_filename":
                try:
                    with open(value, 'a', encoding='utf-8') as f:
                        pass
                except (OSError, PermissionError) as e:
                    raise ValueError(
                        f"Cannot write to '{value}': {e}")

            res[key] = value

        return res
