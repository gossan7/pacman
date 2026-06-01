from .entity import Entity
from .direction import Direction


class Pacman(Entity):

    def __init__(self, direction: Direction = Direction.North) -> None:
        super.__init__(direction)

    def update_direction(self) -> None:
        pass
