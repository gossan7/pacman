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
    """
    Core gameplay engine driving a single Pac-Man playthrough.

    Owns the maze, Pac-Man and the four ghosts, and advances them each
    frame: movement is accumulated as progress towards the next tile,
    gums are eaten, ghost AI targets are chosen, collisions are resolved
    and the intro/outro/death/level timers are ticked. It also applies the
    cheat flags from the shared state and hands control to the score
    registration screen when the game ends.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Build the first level from the configuration.

        Args:
            config: Validated configuration dict (speeds, lives, level
                count, gum values, frightened duration, etc.).
        """
        super().__init__(config)
        self.flag = EngineFlag.GAME
        self.ghost_val: int = config["ghost_val"]
        self.level_max_time: int = config["level_max_time"]
        self.pacman_speed: float = config["pacman_speed"]
        self.ghost_speed: float = config["ghost_speed"]
        self.frightened_duration: float = config["frightened_duration"]
        self.hitbox_radius: float = 0.2
        self.max_levels: int = config["num_levels"]
        self.intro_remaining: float = 0.0
        self.outro_remaining: float = 0.0
        self.death_remaining: float = 0.0
        self.lives: int = self.config["lives"]
        self.score: int = 0
        self.level: int = 1
        self.game_ended: bool = False
        self.won: bool = False
        self._load_level(self.config["seed"])

    def reset(self) -> None:
        """
        Restart a fresh game from level one.

        Resets lives, score, timers and flags, then reloads the first level
        from the configured seed.
        """
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
        """
        Generate a maze and place Pac-Man and the ghosts.

        Pac-Man starts in the middle and one ghost spawns in each corner;
        the level timer and frightened state are reset and the intro
        countdown begins.

        Args:
            seed: Seed passed to the maze generator.
        """
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
        """
        Move on to the next level, or win the game.

        Increments the level counter; if it exceeds the configured maximum
        the game is won and ended, otherwise a new level is loaded.
        """
        self.level += 1
        if self.level > self.max_levels:
            self.won = True
            self.game_ended = True
            return
        seed = 0
        self._load_level(seed)

#    PACMAN

    def _step_pacman(self) -> bool:
        """
        Move Pac-Man one tile in his current or requested direction.

        A pending turn is applied first if the path is open; otherwise he
        keeps his current heading.

        Returns:
            True if Pac-Man moved to a new tile, False if he was blocked.
        """
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
        """
        Eat any gum on a tile and apply its effect.

        Adds the gum's value to the score, removes it, triggers frightened
        mode for a super-gum, and starts the level outro once the last gum
        is eaten.

        Args:
            position: The tile Pac-Man currently occupies.
        """
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
        """
        Move every alive ghost one tile along its chosen direction.

        Ghosts that are travelling back as eyes or respawning are skipped.
        """
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
        """
        Pick the direction a ghost should move this step.

        Args:
            ghost: The ghost to route.

        Returns:
            The fleeing direction when frightened, otherwise the chasing
            direction.
        """
        if ghost.is_edible:
            return self._frightened_direction(ghost)
        return self._chase_direction(ghost)

    def _respawn_ghost(self, ghost: Ghost) -> None:
        """
        Reset a ghost to its spawn tile and alive state.

        Args:
            ghost: The ghost to reset.
        """
        ghost.position = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.prev = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.direction = Direction.NONE
        ghost.is_edible = False
        ghost.mode = GhostMode.ALIVE
        ghost.eyes_remaining = 0.0
        ghost.respawn_remaining = 0.0

    @staticmethod
    def _dist2(a: Vec2, b: Vec2) -> int:
        """
        Return the squared Euclidean distance between two tiles.

        Args:
            a: First tile.
            b: Second tile.

        Returns:
            The squared distance (cheaper than the real distance and
            sufficient for comparisons).
        """
        return (a.row - b.row) ** 2 + (a.col - b.col) ** 2

    def _target_tile(self, ghost: Ghost) -> Vec2:
        """
        Compute the tile a ghost is currently aiming for.

        Each kind targets differently: Blinky aims at Pac-Man, Pinky four
        tiles ahead of him, Inky uses Blinky's position to pick a point
        beyond Pac-Man, and Clyde chases only while far away and otherwise
        retreats to its spawn.

        Args:
            ghost: The ghost whose target is requested.

        Returns:
            The tile the ghost should head towards.
        """
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
        """
        Choose the move that brings a ghost closest to its target.

        Reversing direction is avoided unless it is the only option, and
        ties are broken by the fixed N/W/S/E priority order.

        Args:
            ghost: The ghost to route.

        Returns:
            The best direction, or NONE if the ghost is fully boxed in.
        """
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
        """
        Choose the move that takes a frightened ghost away from Pac-Man.

        Mirrors :meth:`_chase_direction` but maximises distance instead of
        minimising it.

        Args:
            ghost: The frightened ghost to route.

        Returns:
            The fleeing direction, or NONE if the ghost is fully boxed in.
        """
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
        """
        Start frightened mode: make alive ghosts edible and reverse them.
        """
        self.frightened_remaining = self.frightened_duration
        for ghost in self.ghosts:
            if ghost.mode != GhostMode.ALIVE:
                continue
            ghost.is_edible = True
            ghost.direction = OPPOSITE[ghost.direction]

    def _exit_frightened(self) -> None:
        """
        End frightened mode and make every ghost dangerous again.
        """
        self.frightened_remaining = 0.0
        for ghost in self.ghosts:
            ghost.is_edible = False

    def _kill_ghost(self, ghost: Ghost) -> None:
        """
        Award points and send an eaten ghost back as eyes.

        Args:
            ghost: The ghost Pac-Man just ate.
        """
        self.score += self.ghost_val
        ghost.mode = GhostMode.EYES
        ghost.is_edible = False
        ghost.eyes_from = Vec2(ghost.position.row, ghost.position.col)
        ghost.eyes_remaining = _EYES_TIME
        ghost.direction = Direction.NONE

    def _begin_respawn(self, ghost: Ghost) -> None:
        """
        Put a ghost into the respawning state at its spawn tile.

        Args:
            ghost: The ghost whose eyes just reached the spawn.
        """
        ghost.mode = GhostMode.RESPAWNING
        ghost.respawn_remaining = _RESPAWN_TIME
        ghost.position = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.prev = Vec2(ghost.spawn.row, ghost.spawn.col)
        ghost.direction = Direction.NONE

    def _blinky_position(self) -> Vec2:
        """
        Return Blinky's current tile, used for Inky's targeting.

        Returns:
            Blinky's position, or Pac-Man's position if Blinky is absent.
        """
        for ghost in self.ghosts:
            if ghost.kind == GhostKind.BLINKY:
                return ghost.position
        return self.pacman.position

    def _tick_ghost_states(self, dt: float) -> None:
        """
        Advance the eyes and respawn timers of every ghost.

        Eyes that reach their spawn begin respawning; respawning ghosts
        return to the alive state once their timer elapses.

        Args:
            dt: Elapsed time since the previous frame, in seconds.
        """
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
        """
        Count down the frightened timer and end the mode when it expires.

        Args:
            dt: Elapsed time since the previous frame, in seconds.
        """
        if self.frightened_remaining <= 0:
            return
        self.frightened_remaining -= dt
        if self.frightened_remaining <= 0:
            self._exit_frightened()

    def _ahead(self, position: Vec2, direction: Direction, n: int) -> Vec2:
        """
        Return the tile ``n`` steps ahead in a direction.

        Args:
            position: Starting tile.
            direction: Direction to project along.
            n: Number of tiles to advance.

        Returns:
            The projected tile (unchanged if direction is NONE).
        """
        if direction == Direction.NONE:
            return position
        pos = position
        for _ in range(n):
            pos = self.map.destination(pos, direction)
        return pos

    def _current_ghost_speed(self) -> float:
        """
        Return the ghost movement speed for the current state.

        Returns:
            The base ghost speed, halved while frightened mode is active.
        """
        if self.frightened_remaining > 0:
            return self.ghost_speed * _FRIGHTENED_SPEED
        return self.ghost_speed

#    GLOBAL

    def _start_intro(self) -> None:
        """
        Begin the pre-level countdown (freeze then "GO").
        """
        self.intro_remaining = _FREEZE_TIME + _GO_TIME

    def _tick_intro(self, dt: float) -> bool:
        """
        Advance the intro countdown.

        Args:
            dt: Elapsed time since the previous frame, in seconds.

        Returns:
            True while the game should stay frozen, False once play may
            start (or if no intro is running).
        """
        if self.intro_remaining <= 0:
            return False
        self.intro_remaining -= dt
        return self.intro_remaining > _GO_TIME

    def _tick_outro(self, dt: float) -> bool:
        """
        Advance the level-cleared outro and load the next level at its end.

        Args:
            dt: Elapsed time since the previous frame, in seconds.

        Returns:
            True while the outro is playing, False if none is running.
        """
        if self.outro_remaining <= 0:
            return False
        self.outro_remaining -= dt
        if self.outro_remaining <= 0:
            self._advance_level()
        return True

    def _start_death(self) -> None:
        """
        Begin the death animation countdown.
        """
        self.death_remaining = _DEATH_TIME

    def _tick_death(self, dt: float) -> bool:
        """
        Advance the death animation and lose a life when it ends.

        Args:
            dt: Elapsed time since the previous frame, in seconds.

        Returns:
            True while the death animation is playing, False if none is
            running.
        """
        if self.death_remaining <= 0:
            return False
        self.death_remaining -= dt
        if self.death_remaining <= 0:
            self._lose_life()
        return True

    def death_fraction(self) -> float | None:
        """
        Return how far the death animation has progressed.

        Returns:
            A value in [0, 1] for the renderer, or None when no death
            animation is active.
        """
        if self.death_remaining <= 0:
            return None
        frac = 1.0 - max(0.0, self.death_remaining) / _DEATH_TIME
        return min(1.0, max(0.0, frac))

    def intro_label(self) -> str | None:
        """
        Return the intro banner text for the current countdown phase.

        Returns:
            ``"READY ?"`` during the freeze, ``"GO !"`` just before play,
            or None when no intro is running.
        """
        if self.intro_remaining <= 0:
            return None
        if self.intro_remaining > _GO_TIME:
            return "READY ?"
        return "GO !"

    def banner_label(self) -> str | None:
        """
        Return the banner text to overlay on the game view.

        Returns:
            The level-cleared message during the outro, otherwise the
            intro label (which may be None).
        """
        if self.outro_remaining > 0:
            return "CONGRATULATIONS !"
        return self.intro_label()

    def _read_input(self, globalstate: GlobalState) -> None:
        """
        Translate input events into a requested turn or a pause.

        Args:
            globalstate: The shared mutable game state.
        """
        while globalstate.events:
            event = globalstate.events.pop()
            if event in EVENT_TO_DIRECTION:
                self.requested = EVENT_TO_DIRECTION[event]
            if event == EventsEnum.ESCAPE:
                globalstate.to_add = EngineFlag.PAUSE

    def _interp(
            self, prev: Vec2, cur: Vec2, frac: float) -> tuple[float, float]:
        """
        Linearly interpolate between two tiles.

        Args:
            prev: Tile at the start of the step.
            cur: Tile at the end of the step.
            frac: Interpolation factor in [0, 1].

        Returns:
            The (row, col) floating-point position between the two tiles.
        """
        return (prev.row + (cur.row - prev.row) * frac,
                prev.col + (cur.col - prev.col) * frac)

    def smooth_position(
            self, entity: Entity, progress: float) -> tuple[float, float]:
        """
        Compute an entity's smoothed position between two tiles.

        Args:
            entity: The entity to position.
            progress: Accumulated step progress (0 to ``_STEP_COST``).

        Returns:
            The interpolated (row, col) position for rendering.
        """
        return self._interp(
            entity.prev, entity.position, min(1.0, progress / _STEP_COST))

    def ghost_render_position(
            self, ghost: Ghost, progress: float) -> tuple[float, float]:
        """
        Compute a ghost's render position for its current mode.

        Eyes interpolate from where the ghost was eaten towards its spawn,
        respawning ghosts sit on the spawn, and alive ghosts use the normal
        smoothed position.

        Args:
            ghost: The ghost to position.
            progress: Accumulated ghost step progress.

        Returns:
            The (row, col) position for rendering.
        """
        if ghost.mode == GhostMode.EYES:
            frac = 1.0 - max(0.0, ghost.eyes_remaining) / _EYES_TIME
            frac = min(1.0, max(0.0, frac))
            return self._interp(ghost.eyes_from, ghost.spawn, frac)
        if ghost.mode == GhostMode.RESPAWNING:
            return float(ghost.spawn.row), float(ghost.spawn.col)
        return self.smooth_position(ghost, progress)

    def ghost_alpha(self, ghost: Ghost) -> int:
        """
        Compute a ghost's render opacity.

        Args:
            ghost: The ghost to query.

        Returns:
            255 (opaque) for normal ghosts, or a value fading in from 0 to
            255 while the ghost is respawning.
        """
        if ghost.mode != GhostMode.RESPAWNING:
            return 255
        frac = 1.0 - ghost.respawn_remaining / _RESPAWN_TIME
        return int(255 * min(1.0, max(0.0, frac)))

    def _check_collisions(self) -> None:
        """
        Resolve overlaps between Pac-Man and the alive ghosts.

        Uses the smoothed sub-tile positions: an edible ghost is eaten,
        while a dangerous one triggers the death animation.
        """
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
        """
        Deduct a life and reset positions, or end the game.

        Ends the game when no life remains; otherwise Pac-Man and the
        ghosts return to their start tiles and the intro replays.
        """
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
        """
        Count down the per-level time limit.

        Args:
            dt: Elapsed time since the previous frame, in seconds.
        """
        self.level_remaining -= dt
        if self.level_remaining <= 0:
            self._on_timeout()

    def _on_timeout(self) -> None:
        """
        End the game when the level time limit is reached.
        """
        self.game_ended = True

    def _end_game(self, globalstate: GlobalState) -> None:
        """
        Publish the result and switch to the score registration screen.

        Args:
            globalstate: The shared mutable game state.
        """
        globalstate.score = self.score
        globalstate.won = self.won
        globalstate.to_add = EngineFlag.SCORE_REGISTER
        globalstate.focus = EngineFlag.SCORE_REGISTER

    def update_always(self, globalstate: GlobalState) -> None:
        """
        Apply the one-shot cheats that work even without focus.

        Grants an extra life or skips to the next level when the matching
        cheat flag is set, then clears that flag.

        Args:
            globalstate: The shared mutable game state.
        """
        if globalstate.cheats_state["extra_life"]:
            self.lives += 1
            globalstate.cheats_state["extra_life"] = False
        if globalstate.cheats_state["win_level"]:
            globalstate.cheats_state["win_level"] = False
            self._advance_level()

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Advance one frame of gameplay while the game has focus.

        Reads input, runs the death/outro/intro phases (which short-circuit
        normal play), ticks the frightened, level and ghost-state timers,
        then accumulates Pac-Man and ghost movement, eats gums and resolves
        collisions. Honours the speed, ghost-freeze and invincibility
        cheats.

        Args:
            globalstate: The shared mutable game state.
        """
        if self.game_ended:
            self._end_game(globalstate)
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
        self.pacman_progress += self.pacman_speed * \
            (1 if not globalstate.cheats_state["increased_speed"] else 1.5)
        while self.pacman_progress >= _STEP_COST and not self.game_ended:
            if self._step_pacman():
                self.pacman_progress -= _STEP_COST
            else:
                self.pacman_progress = _STEP_COST
                break

        # GHOSTS
        if not globalstate.cheats_state["ghost_freeze"]:
            self.ghost_progress += self._current_ghost_speed()
            while self.ghost_progress >= _STEP_COST and not self.game_ended:
                self.ghost_progress -= _STEP_COST
                self._step_ghosts()

        # EVENTS
        if self.pacman_progress >= _EAT_AT:
            self._eat(self.pacman.position)
        if (not self.game_ended
                and not globalstate.cheats_state["invincibility"]):
            self._check_collisions()
