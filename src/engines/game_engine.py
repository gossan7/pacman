from typing import Any

from .engine import Engine
from ..state import GlobalState
from ..instances import Pacman, Map, Ghost, Entity
from ..state import EngineFlag, GhostKind, GhostMode
from ..pacman_types import Vec2
from ..state import EventsEnum
from ..instances import Direction, SuperGum

EVENT_TO_DIRECTION: dict[EventsEnum, Direction] = {
    EventsEnum.UP: Direction.NORTH,
    EventsEnum.DOWN: Direction.SOUTH,
    EventsEnum.LEFT: Direction.WEST,
    EventsEnum.RIGHT: Direction.EAST
}

_STEP_COST = 100
_EAT_AT = 7 * _STEP_COST // 10
_FREEZE_TIME = 1.5
_GO_TIME = 1.0
_EYES_TIME = 1.0
_OUTRO_TIME = 2.0
_RESPAWN_TIME = 2.0
_DEATH_TIME = 1.0

OPPOSITE = {Direction.NORTH: Direction.SOUTH, Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST, Direction.WEST: Direction.EAST,
            Direction.NONE: Direction.NONE}

_PRIORITY = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)
_FRIGHTENED_SPEED = 0.5


class GameEngine(Engine):

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.GAME
        self.ghost_val: int = config["ghost_val"]
        self.level_max_time: int = config["level_max_time"]
        self.pacman_speed: float = config["pacman_speed"]
        self.ghost_speed: float = config["ghost_speed"]
        self.frightened_duration: float = config["frightened_duration"]
        self.hitbox_radius: float = 0.2
        self.max_levels: int = config["num_levels"]
        self.reset()

    def reset(self) -> None:
        self.intro_remaining: float = 0.0
        self.outro_remaining: float = 0.0
        self.death_remaining: float = 0.0
        self.lives: int = self.config["lives"]
        self.score: int = 0
        self.level: int = 1
        self.game_ended: bool = False
        self.won: bool = False
        self._load_level(self.config["seed"])

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
        self.ghost_progress = 0.0
        self.ghosts = [
            Ghost(Vec2(0, 0), GhostKind.BLINKY),
            Ghost(Vec2(0, self.map.width - 1), GhostKind.PINKY),
            Ghost(Vec2(self.map.height - 1, 0), GhostKind.INKY),
            Ghost(Vec2(self.map.height - 1, self.map.width - 1),
                  GhostKind.CLYDE),
        ]
        self.level_remaining = float(self.level_max_time)
        self.frightened_remaining = 0.0
        self._start_intro()

    def _advance_level(self) -> None:
        self.level += 1
        if self.level > self.max_levels:
            self.won = True
            self.game_ended = True
            return
        seed = 0
        self._load_level(seed)

#    PACMAN

    def _step_pacman(self) -> bool:
        pos = self.pacman.position
        self.pacman.prev = self.pacman.position
        if (self.requested != Direction.NONE
                and self.map.can_move(pos, self.requested)):
            self.pacman.direction = self.requested
            self.requested = Direction.NONE
        if (self.pacman.direction != Direction.NONE
                and self.map.can_move(pos, self.pacman.direction)):
            self.pacman.position = self.map.destination(
                pos, self.pacman.direction)
            return True
        return False

    def _eat(self, position: Vec2) -> None:
        content = self.map.game_map[position.row][position.col].content
        if content is None:
            return
        self.score += content.value
        self.map.delete_content(position.row, position.col)
        if isinstance(content, SuperGum):
            self._enter_frightened()
        if self.map.gums_remaining == 0:
            self.outro_remaining = _OUTRO_TIME

#    GHOSTS

    def _step_ghosts(self) -> None:
        for ghost in self.ghosts:
            if ghost.mode != GhostMode.ALIVE:
                continue
            ghost.prev = ghost.position
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
        ghost.prev = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.direction = Direction.NONE
        ghost.is_edible = False
        ghost.mode = GhostMode.ALIVE
        ghost.eyes_remaining = 0.0
        ghost.respawn_remaining = 0.0

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
        return ghost.spawn

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
        target = self.pacman.position
        opts = [
            d for d in _PRIORITY if self.map.can_move(ghost.position, d)
            and d != OPPOSITE[ghost.direction]]
        if not opts:
            opts = [
                d for d in _PRIORITY if self.map.can_move(ghost.position, d)]
        if not opts:
            return Direction.NONE
        return max(opts, key=lambda d: self._dist2(
            self.map.destination(ghost.position, d), target))

    def _enter_frightened(self) -> None:
        self.frightened_remaining = self.frightened_duration
        for ghost in self.ghosts:
            if ghost.mode != GhostMode.ALIVE:
                continue
            ghost.is_edible = True
            ghost.direction = OPPOSITE[ghost.direction]

    def _exit_frightened(self) -> None:
        self.frightened_remaining = 0.0
        for ghost in self.ghosts:
            ghost.is_edible = False

    def _kill_ghost(self, ghost: Ghost) -> None:
        self.score += self.ghost_val
        ghost.mode = GhostMode.EYES
        ghost.is_edible = False
        ghost.eyes_from = Vec2(ghost.position.row, ghost.position.col)
        ghost.eyes_remaining = _EYES_TIME
        ghost.direction = Direction.NONE

    def _begin_respawn(self, ghost: Ghost) -> None:
        ghost.mode = GhostMode.RESPAWNING
        ghost.respawn_remaining = _RESPAWN_TIME
        ghost.position = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.prev = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.direction = Direction.NONE

    def _blinky_position(self) -> Vec2:
        for ghost in self.ghosts:
            if ghost.kind == GhostKind.BLINKY:
                return ghost.position
        return self.pacman.position

    def _tick_ghost_states(self, dt: float) -> None:
        for ghost in self.ghosts:
            if ghost.mode == GhostMode.EYES:
                ghost.eyes_remaining -= dt
                if ghost.eyes_remaining <= 0:
                    self._begin_respawn(ghost)
            elif ghost.mode == GhostMode.RESPAWNING:
                ghost.respawn_remaining -= dt
                if ghost.respawn_remaining <= 0:
                    ghost.mode = GhostMode.ALIVE

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

    def _current_ghost_speed(self) -> float:
        if self.frightened_remaining > 0:
            return self.ghost_speed * _FRIGHTENED_SPEED
        return self.ghost_speed

#    GLOBAL

    def _start_intro(self) -> None:
        self.intro_remaining = _FREEZE_TIME + _GO_TIME

    def _tick_intro(self, dt: float) -> bool:
        if self.intro_remaining <= 0:
            return False
        self.intro_remaining -= dt
        return self.intro_remaining > _GO_TIME

    def _tick_outro(self, dt: float) -> bool:
        if self.outro_remaining <= 0:
            return False
        self.outro_remaining -= dt
        if self.outro_remaining <= 0:
            self._advance_level()
        return True

    def _start_death(self) -> None:
        self.death_remaining = _DEATH_TIME

    def _tick_death(self, dt: float) -> bool:
        if self.death_remaining <= 0:
            return False
        self.death_remaining -= dt
        if self.death_remaining <= 0:
            self._lose_life()
        return True

    def death_fraction(self) -> float | None:
        if self.death_remaining <= 0:
            return None
        frac = 1.0 - max(0.0, self.death_remaining) / _DEATH_TIME
        return min(1.0, max(0.0, frac))

    def intro_label(self) -> str | None:
        if self.intro_remaining <= 0:
            return None
        if self.intro_remaining > _GO_TIME:
            return "READY ?"
        return "GO !"

    def banner_label(self) -> str | None:
        if self.outro_remaining > 0:
            return "CONGRATULATIONS !"
        return self.intro_label()

    def _read_input(self, globalstate: GlobalState) -> None:
        while globalstate.events:
            event = globalstate.events.pop()
            if event in EVENT_TO_DIRECTION:
                self.requested = EVENT_TO_DIRECTION[event]
            if event == EventsEnum.ESCAPE:
                globalstate.to_add = EngineFlag.PAUSE

    def _interp(
            self, prev: Vec2, cur: Vec2, frac: float) -> tuple[float, float]:
        return (prev.row + (cur.row - prev.row) * frac,
                prev.col + (cur.col - prev.col) * frac)

    def smooth_position(
            self, entity: Entity, progress: float) -> tuple[float, float]:
        return self._interp(
            entity.prev, entity.position, min(1.0, progress / _STEP_COST))

    def ghost_render_position(
            self, ghost: Ghost, progress: float) -> tuple[float, float]:
        if ghost.mode == GhostMode.EYES:
            frac = 1.0 - max(0.0, ghost.eyes_remaining) / _EYES_TIME
            frac = min(1.0, max(0.0, frac))
            return self._interp(ghost.eyes_from, ghost.spawn, frac)
        if ghost.mode == GhostMode.RESPAWNING:
            return float(ghost.spawn.row), float(ghost.spawn.col)
        return self.smooth_position(ghost, progress)

    def ghost_alpha(self, ghost: Ghost) -> int:
        if ghost.mode != GhostMode.RESPAWNING:
            return 255
        frac = 1.0 - ghost.respawn_remaining / _RESPAWN_TIME
        return int(255 * min(1.0, max(0.0, frac)))

    def _check_collisions(self) -> None:
        pr, pc = self._interp(
            self.pacman.prev,
            self.pacman.position,
            self.pacman_progress / _STEP_COST)
        gf = self.ghost_progress / _STEP_COST
        for ghost in self.ghosts:
            if ghost.mode != GhostMode.ALIVE:
                continue
            gr, gc = self._interp(ghost.prev, ghost.position, gf)
            if (pr - gr) ** 2 + (pc - gc) ** 2 >= (2 * self.hitbox_radius)**2:
                continue
            if ghost.is_edible:
                self._kill_ghost(ghost)
            else:
                self._start_death()
                return

    def _lose_life(self) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.game_ended = True
            return
        self.pacman.position = Vec2(*self.map.middle)
        self.pacman.prev = self.pacman.position
        self.pacman.direction = Direction.NONE
        self.requested = Direction.NONE
        self.pacman_progress = 0.0
        self.ghost_progress = 0.0
        for ghost in self.ghosts:
            self._respawn_ghost(ghost)
        self._start_intro()

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
        globalstate.to_add = EngineFlag.SCORE_REGISTER
        globalstate.focus = EngineFlag.SCORE_REGISTER

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        self._read_input(globalstate)
        if self._tick_death(globalstate.delta_time):
            if self.game_ended:
                self._end_game(globalstate)
            return
        if self._tick_outro(globalstate.delta_time):
            if self.game_ended:
                self._end_game(globalstate)
            return
        if self._tick_intro(globalstate.delta_time):
            return
        self._tick_frightened(globalstate.delta_time)
        self._tick_level_timer(globalstate.delta_time)
        self._tick_ghost_states(globalstate.delta_time)

        # PACMAN
        self.pacman_progress += self.pacman_speed
        while self.pacman_progress >= _STEP_COST and not self.game_ended:
            if self._step_pacman():
                self.pacman_progress -= _STEP_COST
            else:
                self.pacman_progress = _STEP_COST
                break

        # GHOSTS
        self.ghost_progress += self._current_ghost_speed()
        while self.ghost_progress >= _STEP_COST and not self.game_ended:
            self.ghost_progress -= _STEP_COST
            self._step_ghosts()

        # EVENTS
        if self.pacman_progress >= _EAT_AT:
            self._eat(self.pacman.position)
        if not self.game_ended:
            self._check_collisions()
        if self.game_ended:
            self._end_game(globalstate)
