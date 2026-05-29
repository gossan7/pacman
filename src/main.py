#!/usr/bin/python3
from typing import Dict

from view import View
from menu import MenuView
from game import GameView
from score import ScoreView


def main() -> None:
    config: Dict = load_config()
    menu_view: View = MenuView(config)
    game_view: View = GameView(config)
    score_view: View = ScoreView(config)

    current_view: View = menu_view

    running = True
    while running:
        current_view.update()
        if current_view.should_end:
            running = False
        current_view = current_view.next_view
