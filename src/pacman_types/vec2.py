from dataclasses import dataclass


@dataclass
class Vec2:
    """
    A simple 2D vector expressed in maze grid coordinates.

    Attributes:
        row: Vertical position (row index in the maze grid).
        col: Horizontal position (column index in the maze grid).
    """

    row: int
    col: int
