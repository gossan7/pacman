from typing import Any
import pyray

from .core import Orchestrator
from .parsers import ScoreParser, ConfigParser


def load_config(filename: str = "config.json") -> dict[str, Any]:
    """hardcoded values to test, need to do a real parser after"""
    res: dict[str, Any] = {
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
        "num_levels": 1,
        "highscore_filename": "highSCORE.json",
    }
    return res


def load_scores(filename: str = "highSCORE.json") -> list[tuple[str, int]]:
    """hardcoded values to test, need to load from the json after"""
    return []


def init_window():
    pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_ERROR)
    pyray.init_window(1920, 1080, "Pacman")
    pyray.hide_cursor()
    width = int(pyray.get_monitor_width(0) / 1.5)
    height = int(pyray.get_monitor_height(0) / 1.5)
    pyray.set_window_size(width, height)
    pyray.set_exit_key(pyray.KeyboardKey.KEY_NULL)


def main() -> None:
    scoreparser = ScoreParser()
    configparser = ConfigParser()
    config: dict[str, Any] = configparser.parse("config.json")
    scores = scoreparser.parse(config["highscore_filename"])
    init_window()
    orchestrator = Orchestrator(config, scores)
    orchestrator.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error has occured during the program: {e}")
