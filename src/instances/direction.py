from enum import IntFlag


class Direction(IntFlag):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
