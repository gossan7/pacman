from abc import ABC, abstractmethod
from .direction import Direction
import random


class Entity(ABC):

    def __init__(self, direction: Direction = Direction.NONE) -> None:
        """Encode directions on 4 bits
        like 1: top | 2: east | 4 : bottom | 8 : west to mimic
        the mazegenerator and do bitwise operations"""
        self.direction: Direction = direction

    @staticmethod
    def is_valid_direction(value: int) -> bool:
        """Maybe overkill, used to validate a direction"""
        return value != 0 and (value & (value - 1)) == 0 and value <= 8

    def _choose_random(
            self,
            possible_directions: list[Direction]) -> Direction:
        """Placeholder-like to generate a random walk,
        the list of directions is supposed to be a list of valid directions
        (need a map and a position to do so) given by the GameEngine
        """
        return random.choice(possible_directions)

    @abstractmethod
    def update_direction(self) -> None:
        """For pacman : changes the direction based on inputs
        For ghosts : passing a map then updating according to behaviour"""
        pass
