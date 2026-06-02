from typing import Dict, Any
from .engines import Orchestrator


# from view import View
# from menu import MenuView
# from game import GameView
# from score import ScoreView


def load_config(filename: str = "config.json") -> Dict:
    """hardcoded values to test, need to do a real parser after"""
    res: dict[str, Any] = {
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
    config: Dict = load_config()

    orchestrator = Orchestrator(config, 1.0)
    orchestrator.run()


# def main() -> None:
#     config: Dict = load_config()
#     menu_view: View = MenuView(config)
#     game_view: View = GameView(config)
#     score_view: View = ScoreView(config)

#     current_view: View = menu_view

#     running = True
#     while running:
#         current_view.update()
#         if current_view.should_end:
#             running = False
#         current_view = current_view.next_view
