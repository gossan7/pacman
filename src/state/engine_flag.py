from enum import IntFlag


class EngineFlag(IntFlag):
    NONE = 0
    MENU = 1
    GAME = 2
    PAUSE = 4
    CHEAT = 8
    SCORE = 16
