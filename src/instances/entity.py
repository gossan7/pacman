from abc import ABC
from .direction import Direction
from ..pacman_types import Vec2


class Entity(ABC):
    def __init__(
            self,
            position: Vec2,
            direction: Direction = Direction.NONE
    ) -> None:
        """Encode directions on 4 bits
        like 1: top | 2: east | 4 : bottom | 8 : west to mimic
        the mazegenerator and do bitwise operations"""
        self.direction: Direction = direction
        self.position: Vec2 = position

    @staticmethod
    def is_valid_direction(value: int) -> bool:
        """Maybe overkill, used to validate a direction"""
        return value != 0 and (value & (value - 1)) == 0 and value <= 8

    def update_direction(self, direction: Direction) -> None:
        self.direction = direction
