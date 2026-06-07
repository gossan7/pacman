from typing import Any
import pyray

from .renderer import Renderer
from ..engines import GameEngine
from .window_handler import WindowHandler, WORLD_WIDTH, WORLD_HEIGHT
from ..instances import Direction, SuperGum
from ..state import GhostKind


HUD_HEIGHT = 90
MARGIN = 20
HUD_FONT = 36
HUD_SPACING = 60
STEP_COST = 100
# Note: faut laisser le meme step_cost que dans l'engine

WALL_COLOR = pyray.Color(33, 33, 222, 255)
GUM_COLOR = pyray.Color(255, 220, 180, 255)
FRIGHTENED_COLOR = pyray.Color(36, 36, 255, 255)
EYE_COLOR = pyray.WHITE
PUPIL_COLOR = pyray.Color(20, 20, 120, 255)

GHOST_COLORS = {
    GhostKind.BLINKY: pyray.Color(255, 0, 0, 255),
    GhostKind.PINKY: pyray.Color(255, 184, 255, 255),
    GhostKind.INKY: pyray.Color(0, 255, 255, 255),
    GhostKind.CLYDE: pyray.Color(255, 184, 82, 255),
}

_EYE_DIR = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
    Direction.EAST: (1, 0),
    Direction.NONE: (0, 0),
}


class GameRenderer(Renderer):
    def __init__(
            self,
            config: dict[str, Any],
            engine: GameEngine,
            window_handler: WindowHandler
    ) -> None:
        self.config = config
        self.engine: GameEngine = engine
        self.window_handler = window_handler
        self._anim: dict[Any, tuple[tuple[int, int], tuple[int, int]]] = {}

    def _smooth(self, key: Any, position: Any, progress: float) -> tuple:
        cur = (position.row, position.col)
        start, seen, last = self._anim.get(key, (cur, cur, progress))
        if progress < last:
            if cur == seen:
                start = cur
            elif abs(cur[0] - seen[0]) + abs(cur[1] - seen[1]) > 1:
                start = cur
            else:
                start = seen
            seen = cur
        self._anim[key] = (start, seen, progress)
        frac = min(1.0, progress / STEP_COST)
        row = start[0] + (cur[0] - start[0]) * frac
        col = start[1] + (cur[1] - start[1]) * frac
        return row, col

    def render(self) -> None:
        to_screen = self.window_handler.to_screen
        pyray.clear_background(pyray.BLACK)

        game_map = self.engine.map
        cols, rows = game_map.width, game_map.height
        area_w = WORLD_WIDTH - 2 * MARGIN
        area_h = WORLD_HEIGHT - HUD_HEIGHT - 2 * MARGIN
        cell = max(1, min(area_w // cols, area_h // rows))
        thick = max(2, cell // 8)
        ox = (WORLD_WIDTH - cell * cols) // 2
        oy = HUD_HEIGHT + MARGIN + (area_h - cell * rows) // 2
        radius = int(cell * 0.42)
        half = cell // 2

        # MAP
        for row in range(rows):
            for col in range(cols):
                board = game_map.game_map[row][col]
                x, y = ox + col * cell, oy + row * cell
                edges = (
                    (Direction.NORTH, x, y, cell, thick),
                    (Direction.SOUTH, x, y + cell - thick, cell, thick),
                    (Direction.WEST, x, y, thick, cell),
                    (Direction.EAST, x + cell - thick, y, thick, cell),
                )
                for bit, ex, ey, ew, eh in edges:
                    if board.walls & bit:
                        pyray.draw_rectangle(
                            to_screen(ex), to_screen(ey),
                            to_screen(ew), to_screen(eh), WALL_COLOR)
                if board.content is not None:
                    gum_r = (int(cell * 0.28)
                             if isinstance(board.content, SuperGum)
                             else max(1, int(cell * 0.10)))
                    pyray.draw_circle(
                        to_screen(x + half), to_screen(y + half),
                        to_screen(gum_r), GUM_COLOR)

        # PACMAN
        pac = self.engine.pacman
        prow, pcol = self._smooth("pac", pac.position,
                                  self.engine.pacman_progress)
        pcx = ox + int(pcol * cell) + half
        pcy = oy + int(prow * cell) + half
        pyray.draw_circle(
            to_screen(pcx), to_screen(pcy), to_screen(radius), pyray.YELLOW)

        # GHOSTS
        for ghost in self.engine.ghosts:
            grow, gcol = self._smooth(ghost.kind, ghost.position,
                                      self.engine.ghost_progress)
            gx = ox + int(gcol * cell) + half
            gy = oy + int(grow * cell) + half
            color = (FRIGHTENED_COLOR if ghost.is_edible
                     else GHOST_COLORS[ghost.kind])
            pyray.draw_circle(
                to_screen(gx), to_screen(gy), to_screen(radius), color)

            dx, dy = _EYE_DIR.get(ghost.direction, (0, 0))
            eye_r = max(1, int(radius * 0.30))
            pupil_r = max(1, int(radius * 0.15))
            gap = int(radius * 0.40)
            look = int(radius * 0.18)
            ey = gy - int(radius * 0.10)
            for side in (-1, 1):
                ex = gx + side * gap
                pyray.draw_circle(
                    to_screen(ex), to_screen(ey), to_screen(eye_r),
                    EYE_COLOR)
                pyray.draw_circle(
                    to_screen(ex + dx * look), to_screen(ey + dy * look),
                    to_screen(pupil_r), PUPIL_COLOR)

        # HUD
        font = to_screen(HUD_FONT)
        engine = self.engine
        items = [
            f"SCORE {engine.score}",
            f"LEVEL {engine.level}",
            f"LIVES {engine.lives}",
            f"TIME {max(0, int(engine.level_remaining))}",
        ]
        hx, hy = to_screen(MARGIN), to_screen(MARGIN)
        for text in items:
            pyray.draw_text(text, hx, hy, font, pyray.WHITE)
            hx += pyray.measure_text(text, font) + to_screen(HUD_SPACING)
