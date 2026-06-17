from typing import Any
import pyray

from .core import Orchestrator
from .parsers import ScoreParser, ConfigParser


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
    config: dict[str, Any] = configparser.parse("config")
    scores = scoreparser.parse(config["highscore_filename"])
    init_window()
    orchestrator = Orchestrator(config, scores)
    orchestrator.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error has occured during the program: {e}")
