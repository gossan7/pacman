from typing import Any
import pyray

from .core import Orchestrator


def load_config(filename: str = "config.json") -> dict[str, Any]:
    """hardcoded values to test, need to do a real parser after"""
    res: dict[str, Any] = {
        "fps": 30,
        "seed": 42,
        "width": 10,
        "height": 10,
        "lives": 3,
        "gum_val": 10,
        "supergum_val": 50,
        "ghost_val": 200,
        "level_max_time": 90,
        "frightened_duration": 7.0,
        "pacman_speed": 15,
        "ghost_speed": 7,
        "num_levels": 10,
        "highscore_filename": "highSCORE.json",
    }
    return res


def init_window():
    pyray.init_window(1920, 1080, "Pacman")
    width = int(pyray.get_monitor_width(0) / 1.5)
    height = int(pyray.get_monitor_height(0) / 1.5)
    pyray.set_window_size(width, height)


def main() -> None:
    config: dict[str, Any] = load_config()
    init_window()
    orchestrator = Orchestrator(config)
    orchestrator.run()
    # orchestrator.run_test()


if __name__ == "__main__":
    main()
