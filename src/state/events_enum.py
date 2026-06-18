from enum import Enum


class EventsEnum(Enum):
    """
    Abstract input events produced from raw key presses.

    Engines react to these high-level events instead of physical keys, so
    the key bindings can change without touching the engine logic.
    """

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    ENTER = 4
    ESCAPE = 5
    FULLSCREEN = 6
    BACKSPACE = 7
