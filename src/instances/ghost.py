from .entity import Entity
from .direction import Direction
from ..pacman_types import Vec2
from ..state import GhostKind, GhostMode


class Ghost(Entity):
    """
    A ghost entity with its spawn point, kind and lifecycle state.

    Tracks whether the ghost is currently edible (frightened) and the
    timers used while it travels back to spawn as eyes and respawns.
    """

    def __init__(
            self,
            position: Vec2,
            ghost_kind: GhostKind,
            direction: Direction = Direction.NONE,
    ) -> None:
        """
        Initialise a ghost at its spawn cell.

        Args:
            position: Spawn cell, also remembered as the respawn point.
            ghost_kind: Which ghost this is (Blinky, Pinky, Inky, Clyde).
            direction: Initial facing direction (defaults to NONE).
        """
        super().__init__(position, direction)
        self.is_edible: bool = False
        self.spawn: Vec2 = Vec2(position.row, position.col)
        self.kind: GhostKind = ghost_kind
        self.mode: GhostMode = GhostMode.ALIVE
        self.eyes_from: Vec2 = Vec2(position.row, position.col)
        self.eyes_remaining: float = 0.0
        self.respawn_remaining: float = 0.0
