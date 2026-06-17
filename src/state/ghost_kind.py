from enum import Enum


class GhostKind(Enum):
    """
    The four ghosts, each with its own targeting behaviour.

    Blinky chases Pac-Man directly, Pinky ambushes ahead of him, Inky
    is unpredictable and Clyde alternates between chasing and scattering.
    """

    BLINKY = 0
    PINKY = 1
    INKY = 2
    CLYDE = 3
