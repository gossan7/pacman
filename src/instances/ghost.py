from .entity import Entity
from .direction import Direction


class Ghost(Entity):

    def __init__(self, direction: Direction = Direction.NORTH) -> None:
        super().__init__(direction)

    def update_direction(self, possible_directions: list[Direction]) -> None:
        self._choose_random(possible_directions)
