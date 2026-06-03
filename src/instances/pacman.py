from .entity import Entity
from .direction import Direction
from ..pacman_types import Vec2


class Pacman(Entity):
    def __init__(
            self,
            position: Vec2,
            direction: Direction = Direction.NORTH
    ) -> None:
        super().__init__(position, direction)

    def update_direction(self, possible_directions: list[Direction]) -> None:
        pass
