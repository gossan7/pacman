from enum import IntFlag


class Direction(IntFlag):
    """
    Cardinal movement directions encoded as bit flags.

    The values match the wall encoding used by the maze generator
    (1: north, 2: east, 4: south, 8: west) so directions and walls can be
    combined with bitwise operations.
    """

    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
