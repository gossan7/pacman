from enum import IntFlag


class EngineFlag(IntFlag):
    """
    Identifies each engine/screen so it can be tracked on the engine stack.

    The orchestrator uses these values to decide which engine currently has
    focus and which one should be pushed onto or popped from the stack.
    """

    NONE = 0
    MENU = 1
    GAME = 2
    SCORES = 3
    CONTROLS = 4
    OPTIONS = 5
    QUIT = 6
    PAUSE = 7
    CHEAT = 8
    SCORE_REGISTER = 9
