import os
import sys
from typing import Any
import pyray

from .core import Orchestrator
from .parsers import ScoreParser, ConfigParser


def init_window() -> None:
    """
    Create and configure the game window.

    Opens the raylib window, hides the cursor, scales it to a fraction of
    the monitor size and disables the default exit key so escape can be
    handled by the engines.
    """
    pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_ERROR)
    pyray.init_window(1920, 1080, "Pacman")
    pyray.hide_cursor()
    width = int(pyray.get_monitor_width(0) / 1.5)
    height = int(pyray.get_monitor_height(0) / 1.5)
    pyray.set_window_size(width, height)
    pyray.set_exit_key(pyray.KeyboardKey.KEY_NULL)


def main() -> None:
    """
    Entry point: load config and scores, then run the game.

    Parses the configuration and highscore files, initialises the window
    and hands control to the orchestrator's main loop.
    """
    frozen = getattr(sys, "frozen", False)
    if frozen:
        os.chdir(os.path.dirname(sys.executable))
    args = sys.argv[1:]
    if len(args) > 1:
        print("Error: too many arguments. Expected a single config file.")
        return
    if args:
        config_path = args[0]
    elif frozen:
        config_path = "config"
    else:
        print("Usage: python3 pac-man.py <config file>")
        return
    scoreparser = ScoreParser()
    configparser = ConfigParser()
    config: dict[str, Any] = configparser.parse(config_path)
    scores = scoreparser.parse(config["highscore_filename"])
    init_window()
    orchestrator = Orchestrator(config, scores)
    orchestrator.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error has occured during the program: {e}")
