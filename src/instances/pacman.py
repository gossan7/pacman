from .entity import Entity
from .direction import Direction
from ..pacman_types import Vec2


class Pacman(Entity):
    """
    The player-controlled Pac-Man entity.

    A plain Entity with no extra state of its own; movement and lives are
    handled by the game engine.
    """

    def __init__(
            self,
            position: Vec2,
            direction: Direction = Direction.NONE
    ) -> None:
        """
        Initialise Pac-Man at a grid cell.

        Args:
            position: Starting cell of the player.
            direction: Initial facing direction (defaults to NONE).
        """
        super().__init__(position, direction)
