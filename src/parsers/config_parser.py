import json
from typing import Any

_CONFIG_CONTENT = {
    "fps": int,
    "seed": int,
    "width": int,
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
    "height": 10,
    "lives": 3,
    "gum_val": 10,
    "supergum_val": 50,
    "ghost_val": 200,
    "level_max_time": 90,
    "frightened_duration": 7.0,
    "pacman_speed": 10,
    "ghost_speed": 6,
    "num_levels": 10,
    "highscore_filename": "highSCORE.json"
}


class ConfigParser:
    """
    Loads and validates the game configuration from a JSON file.

    The parser strips ``#`` comment lines, falls back to sensible defaults
    for any missing, malformed or out-of-range key, and never raises on bad
    input so the game can always start.
    """

    @staticmethod
    def _strip_comments(text: str) -> str:
        """
        Remove full-line ``#`` comments from raw config text.

        Args:
            text: The raw file contents.

        Returns:
            The text with comment-only lines dropped.
        """
        lines = []
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                continue
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _writable(path: str) -> bool:
        """
        Check that a file path can be opened for writing.

        Args:
            path: The candidate file path.

        Returns:
            True if the path can be opened in append mode without error.
        """
        try:
            with open(path, 'a', encoding='utf-8'):
                pass
        except (OSError, ValueError):
            return False
        return True

    @staticmethod
    def _valid_value(key: str, value: Any) -> bool:
        """
        Validate a config value against the rules for its key.

        Args:
            key: The configuration key being checked.
            value: The candidate value (already of the expected type).

        Returns:
            True if the value is within the allowed range for that key.
        """
        if key == "fps":
            return bool(30 <= value <= 60)
        if key == "num_levels":
            return bool(value >= 10)
        if key in ("width", "height"):
            return bool(value >= 10)
        if key in ("lives", "num_levels", "level_max_time",
                   "pacman_speed", "ghost_speed"):
            return bool(value > 0)
        if key in ("gum_val", "supergum_val", "ghost_val"):
            return bool(value >= 0)
        if key == "frightened_duration":
            return bool(value > 0.0)
        if key == "highscore_filename":
            return ConfigParser._writable(value)
        return True

    def parse(self, filename: str) -> dict[str, Any]:
        """
        Parse a configuration file into a complete config dict.

        Missing or invalid keys are reported with a warning and replaced by
        their default value; the method never raises on bad input.

        Args:
            filename: Path to the JSON (with ``#`` comments) config file.

        Returns:
            A dict with every config key set to a valid value.
        """
        res: dict[str, Any] = dict(_DEFAULT_CONFIG)

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                raw = f.read()
        except FileNotFoundError:
            print(f"Warning: Config file '{filename}' not found. "
                  f"Using default config.")
            return res
        except Exception as e:
            print(f"Warning: Could not read config file '{filename}': {e}. "
                  f"Using default config.")
            return res

        try:
            content = json.loads(self._strip_comments(raw))
        except (ValueError, RecursionError) as e:
            print(f"Warning: Config file '{filename}' is not valid JSON: {e}. "
                  f"Using default config.")
            return res

        if not isinstance(content, dict):
            print("Warning: Config must be a JSON object (dict). "
                  "Using default config.")
            return res

        for key in _CONFIG_CONTENT:
            if key not in content:
                print(f"Warning: missing config key '{key}'; "
                      f"using default {_DEFAULT_CONFIG[key]}.")

        for key, value in content.items():
            if key not in _CONFIG_CONTENT:
                print(f"Warning: unknown config key '{key}' ignored.")
                continue

            expected = _CONFIG_CONTENT[key]
            if expected is float and isinstance(value, int) \
                    and not isinstance(value, bool):
                value = float(value)

            if isinstance(value, bool) or not isinstance(value, expected):
                print(f"Warning: '{key}' must be {expected.__name__}; "
                      f"keeping default {_DEFAULT_CONFIG[key]}.")
                continue

            if not self._valid_value(key, value):
                print(f"Warning: invalid value for '{key}' ({value}); "
                      f"keeping default {_DEFAULT_CONFIG[key]}.")
                continue

            res[key] = value

        return res
