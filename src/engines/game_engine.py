from typing import Any

from .engine import Engine
from ..state import GlobalState
from ..instances import Pacman, Map, Ghost
from ..state import EngineFlag
from ..pacman_types import Vec2
from ..state import EventsEnum
from ..instances import Direction

EVENT_TO_DIRECTION: dict[EventsEnum, Direction] = {
    EventsEnum.UP: Direction.NORTH,
    EventsEnum.DOWN: Direction.SOUTH,
    EventsEnum.LEFT: Direction.WEST,
    EventsEnum.RIGHT: Direction.EAST
}

_STEP_COST = 100 

class GameEngine(Engine):
    def __init__(
            self,
            config: dict[str, Any],
    ) -> None:
        super().__init__(config)
        self.flag = EngineFlag.GAME
        self.map: Map = Map(
            gum_val=config["gum_val"],
            supergum_val=config["supergum_val"],
            width=config["width"],
            height=config["height"],
            seed=config["seed"]
        )

        self.ghost_val: int = config["ghost_val"]
        self.level_max_time: int = config["level_max_time"]
        self.lives: int = config["lives"]

        self.pacman: Pacman = Pacman(Vec2(*self.map.middle))
        self.requested: Direction = Direction.NONE
        self.pacman_progress: float = 0.0
        self.pacman_speed: float = config["pacman_speed"]

        self.ghosts = [
            Ghost(Vec2(0, 0)),
            Ghost(Vec2(0, self.map.width - 1)),
            Ghost(Vec2(self.map.height - 1, 0)),
            Ghost(Vec2(self.map.height - 1, self.map.width - 1))
        ]

    def _read_input(self, globalstate: GlobalState) -> None:
        for event in globalstate.events:
            if event in EVENT_TO_DIRECTION:
                self.requested = EVENT_TO_DIRECTION[event]

    def _step_pacman(self) -> None:
        pos = self.pacman.position
        if self.requested != Direction.NONE and self.map.can_move(
                pos, self.requested):
            self.pacman.direction = self.requested
            self.requested = Direction.NONE
        if (self.pacman.direction != Direction.NONE
                and self.map.can_move(pos, self.pacman.direction)):
            self.pacman.position = self.map.destination(
                pos, self.pacman.direction)

    def update_always(self, globalstate: GlobalState) -> None:
        # rien a priori
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        self._read_input(globalstate)
        self.pacman_progress += self.pacman_speed
        while self.pacman_progress >= _STEP_COST:
            self.pacman_progress -= _STEP_COST
            self._step_pacman()