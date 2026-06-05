from typing import Any

from .engine import Engine
from ..state import GlobalState
from ..instances import Pacman, Map, Ghost
from ..state import EngineFlag, GhostKind
from ..pacman_types import Vec2
from ..state import EventsEnum
from ..instances import Direction, SuperGum
import random

EVENT_TO_DIRECTION: dict[EventsEnum, Direction] = {
    EventsEnum.UP: Direction.NORTH,
    EventsEnum.DOWN: Direction.SOUTH,
    EventsEnum.LEFT: Direction.WEST,
    EventsEnum.RIGHT: Direction.EAST
}

_STEP_COST = 100

OPPOSITE = {Direction.NORTH: Direction.SOUTH, Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST, Direction.WEST: Direction.EAST,
            Direction.NONE: Direction.NONE}

_PRIORITY = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)


class GameEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.GAME
        # --- état de PARTIE (conservé entre niveaux) ---
        self.ghost_val: int = config["ghost_val"]
        self.level_max_time: int = config["level_max_time"]
        self.pacman_speed: float = config["pacman_speed"]
        self.frightened_duration: float = config["frightened_duration"]
        self.lives: int = config["lives"]
        self.score: int = 0
        self.level: int = 1

        self.game_ended: bool = False
        self.max_levels: int = config["num_levels"]
        self.won: bool = False
        # --- état de NIVEAU (réinitialisé à chaque niveau) ---
        self._load_level(config["seed"])

    def _load_level(self, seed: int) -> None:
        self.map = Map(
            gum_val=self.config["gum_val"],
            supergum_val=self.config["supergum_val"],
            width=self.config["width"],
            height=self.config["height"],
            seed=seed)
        self.pacman = Pacman(Vec2(*self.map.middle))
        self.requested = Direction.NONE
        self.pacman_progress = 0.0
        self.ghosts = [
            Ghost(Vec2(0, 0), GhostKind.BLINKY),
            Ghost(Vec2(0, self.map.width - 1), GhostKind.PINKY),
            Ghost(Vec2(self.map.height - 1, 0), GhostKind.INKY),
            Ghost(Vec2(self.map.height - 1, self.map.width - 1),
                  GhostKind.CLYDE),
        ]
        self.level_remaining = float(self.level_max_time)
        self.frightened_remaining = 0.0

    def _advance_level(self) -> None:
        self.level += 1
        if self.level > self.max_levels:
            self.won = True
            self.game_ended = True
            return
        seed = random.randrange(2 ** 31)   # voir s'il faut pas mettre juste 0
        self._load_level(seed)

#    PACMAN

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
            self._eat(self.pacman.position)

    def _eat(self, position: Vec2) -> None:
        content = self.map.game_map[position.row][position.col].content
        if content is None:
            return
        self.score += content.value
        self.map.delete_content(position.row, position.col)
        if isinstance(content, SuperGum):
            self._enter_frightened()
        if self.map.gums_remaining == 0:
            self._advance_level()

#    GHOSTS

    def _step_ghosts(self) -> None:
        for ghost in self.ghosts:
            direction = self._choose_direction(ghost)
            if direction != Direction.NONE and self.map.can_move(
                    ghost.position, direction):
                ghost.direction = direction
                ghost.position = self.map.destination(
                    ghost.position, direction)

    def _choose_direction(self, ghost: Ghost) -> Direction:
        if ghost.is_edible:
            return self._frightened_direction(ghost)
        return self._chase_direction(ghost)

    def _respawn_ghost(self, ghost: Ghost) -> None:
        ghost.position = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.direction = Direction.NONE
        ghost.is_edible = False

    @staticmethod
    def _dist2(a: Vec2, b: Vec2) -> int:
        return (a.row - b.row) ** 2 + (a.col - b.col) ** 2

    def _target_tile(self, ghost: Ghost) -> Vec2:
        pac = self.pacman.position
        if ghost.kind == GhostKind.BLINKY:
            return pac
        if ghost.kind == GhostKind.PINKY:
            return self._ahead(pac, self.pacman.direction, 4)
        if ghost.kind == GhostKind.INKY:
            two = self._ahead(pac, self.pacman.direction, 2)
            b = self._blinky_position()
            return Vec2(2 * two.row - b.row, 2 * two.col - b.col)
        if ghost.kind == GhostKind.CLYDE:
            if self._dist2(ghost.position, pac) > 8 * 8:
                return pac
        return ghost.scatter_corner

    def _chase_direction(self, ghost: Ghost) -> Direction:
        target = self._target_tile(ghost)
        opts = [d for d in _PRIORITY
                if self.map.can_move(ghost.position, d)
                and d != OPPOSITE[ghost.direction]]
        if not opts:
            opts = [d for d in _PRIORITY
                    if self.map.can_move(ghost.position, d)]
        if not opts:
            return Direction.NONE
        return min(opts, key=lambda d: self._dist2(
            self.map.destination(ghost.position, d), target))

    def _frightened_direction(self, ghost: Ghost) -> Direction:
        opts = [d for d in self.map.open_directions(ghost.position)
                if d != OPPOSITE[ghost.direction]]
        if not opts:
            opts = self.map.open_directions(ghost.position)
        if not opts:
            return Direction.NONE
        return random.choice(opts)

    def _enter_frightened(self) -> None:
        self.frightened_remaining = self.frightened_duration
        for ghost in self.ghosts:
            ghost.is_edible = True
            ghost.direction = OPPOSITE[ghost.direction]

    def _exit_frightened(self) -> None:
        self.frightened_remaining = 0.0
        for ghost in self.ghosts:
            ghost.is_edible = False

    def _blinky_position(self) -> Vec2:
        for ghost in self.ghosts:
            if ghost.kind == GhostKind.BLINKY:
                return ghost.position
        return self.pacman.position

    def _tick_frightened(self, dt: float) -> None:
        if self.frightened_remaining <= 0:
            return
        self.frightened_remaining -= dt
        if self.frightened_remaining <= 0:
            self._exit_frightened()

    def _ahead(self, position: Vec2, direction: Direction, n: int) -> Vec2:
        if direction == Direction.NONE:
            return position
        pos = position
        for _ in range(n):
            pos = self.map.destination(pos, direction)
        return pos

#    GLOBAL

    def _read_input(self, globalstate: GlobalState) -> None:
        for event in globalstate.events:
            if event in EVENT_TO_DIRECTION:
                self.requested = EVENT_TO_DIRECTION[event]

    def _check_collisions(self) -> None:
        for ghost in self.ghosts:
            if ghost.position != self.pacman.position:
                continue
            if ghost.is_edible:
                self.score += self.ghost_val
                self._respawn_ghost(ghost)
            else:
                self._lose_life()
                return

    def _lose_life(self) -> None:
        self.lives -= 1
        self.pacman.position = Vec2(*self.map.middle)
        self.pacman.direction = Direction.NONE
        self.requested = Direction.NONE
        self.pacman_progress = 0.0
        if self.lives <= 0:
            self.game_ended = True

    def _tick_level_timer(self, dt: float) -> None:
        self.level_remaining -= dt
        if self.level_remaining <= 0:
            self._on_timeout()

    def _on_timeout(self) -> None:
        # faudra qu'on décide: game over ou restart le level ?
        # je mets game over pour l'instant ca semble mieux
        self.game_ended = True

    def _end_game(self, globalstate: GlobalState) -> None:
        globalstate.score = self.score
        globalstate.won = self.won
        globalstate.to_add = EngineFlag.SCORE
        globalstate.focus = EngineFlag.SCORE

    def update_always(self, globalstate: GlobalState) -> None:
        # rien a priori
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        self._read_input(globalstate)
        self._tick_frightened(globalstate.delta_time)
        self._tick_level_timer(globalstate.delta_time)
        self.pacman_progress += self.pacman_speed
        while self.pacman_progress >= _STEP_COST:
            self.pacman_progress -= _STEP_COST
            self._step_pacman()
            self._step_ghosts()
            self._check_collisions()
            if self.game_ended:
                break
        if self.game_ended:
            self._end_game(globalstate)
