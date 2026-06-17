from abc import ABC
from .direction import Direction
from ..pacman_types import Vec2


class Entity(ABC):
    """
    Abstract base for anything that occupies and moves on the maze grid.

    Directions are encoded on 4 bits (1: top, 2: east, 4: bottom, 8: west)
    to mimic the maze generator and allow bitwise operations. Pacman and
    Ghost inherit from this class.
    """

    def __init__(
            self,
            position: Vec2,
            direction: Direction = Direction.NONE
    ) -> None:
        """
        Initialise the entity at a grid cell.

        Args:
            position: Starting cell of the entity.
            direction: Initial facing direction (defaults to NONE).
        """
        self.direction: Direction = direction
        self.position: Vec2 = position
        self.prev: Vec2 = Vec2(position.row, position.col)

    @staticmethod
    def is_valid_direction(value: int) -> bool:
        """
        Check that a value encodes exactly one cardinal direction.

        Args:
            value: The integer to validate.

        Returns:
            True if exactly one of the four direction bits is set.
        """
        return value != 0 and (value & (value - 1)) == 0 and value <= 8

    def update_direction(self, direction: Direction) -> None:
        """
        Set the entity's current facing direction.

        Args:
            direction: The new direction to face.
        """
        self.direction = direction
