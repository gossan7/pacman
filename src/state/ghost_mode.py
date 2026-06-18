from enum import Enum, auto


class GhostMode(Enum):
    """
    Lifecycle state of a ghost.

    ALIVE means the ghost roams normally, EYES means it was eaten and is
    travelling back to its spawn as a pair of eyes, and RESPAWNING means it
    is waiting at the spawn before becoming active again.
    """

    ALIVE = auto()
    EYES = auto()
    RESPAWNING = auto()
