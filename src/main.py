from typing import Any
from .core import Orchestrator


def load_config(filename: str = "config.json") -> dict:
    """hardcoded values to test, need to do a real parser after"""
    res: dict[str, Any] = {
        "fps": 30,
        "seed": 42,
        "width": 20,
        "height": 20,
        "lives": 3,
        "gum_val": 10,
        "supergum_val": 50,
        "ghost_val": 200,
        "level_max_time": 90,
        "highscore_filename": "highscores.json",
    }
    return res


def main() -> None:
    config: dict = load_config()

    orchestrator = Orchestrator(config)
    orchestrator.run()
    # orchestrator.run_test()
