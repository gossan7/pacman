from typing import Any
import pyray

from .renderer import Renderer
from ..engines import GameEngine
from .window_handler import WindowHandler, WORLD_WIDTH, WORLD_HEIGHT
from ..instances import Direction, SuperGum, Ghost
from ..state import GhostKind


HUD_HEIGHT = 90
MARGIN = 20
HUD_FONT = 36
HUD_SPACING = 60

PACMAN_SHEET = "assets/pacman.png"
GHOSTS_SHEET = "assets/ghosts.png"

WALL_COLOR = pyray.Color(33, 33, 222, 255)
GUM_COLOR = pyray.Color(255, 220, 180, 255)

SPRITE_PX = 14
SPRITE_SCALE = 0.85

PAC_COLS = 3
PAC_FRAMES = {
    Direction.SOUTH: (2, 0, 1),
    Direction.WEST: (2, 3, 4),
    Direction.EAST: (2, 5, 6),
    Direction.NORTH: (2, 7, 8),
    Direction.NONE: (2, 5, 6),
}
_CHOMP = (0, 1, 2, 1)

GHOST_BASE_ROW = {
    GhostKind.BLINKY: 0,
    GhostKind.CLYDE: 4,
    GhostKind.INKY: 8,
    GhostKind.PINKY: 12,
}
DIR_OFFSET = {
    Direction.SOUTH: 0,
    Direction.WEST: 1,
    Direction.EAST: 2,
    Direction.NORTH: 3,
}
FRIGHTENED_ROW = 18
FRIGHTENED_FLASH_ROW = 19
FLASH_AT = 2.0

_FRAMES_ANIMATION = 30


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
        self.frame: int = 0
        self.pac_sheet = self._load_sheet(PACMAN_SHEET)
        self.ghost_sheet = self._load_sheet(GHOSTS_SHEET)

    def _load_sheet(self, path: str) -> pyray.Texture:
        img = pyray.load_image(path)
        pyray.image_color_replace(img, pyray.BLACK, pyray.BLANK)
        tex = pyray.load_texture_from_image(img)
        pyray.unload_image(img)
        pyray.set_texture_filter(tex, pyray.TEXTURE_FILTER_POINT)
        return tex

    def unload(self) -> None:
        pyray.unload_texture(self.pac_sheet)
        pyray.unload_texture(self.ghost_sheet)

    def _draw_sprite(
            self, sheet: pyray.Texture, col: int, row: int,
            cx: int, cy: int, size: int) -> None:
        src = pyray.Rectangle(
            col * SPRITE_PX, row * SPRITE_PX, SPRITE_PX, SPRITE_PX)
        dst = pyray.Rectangle(cx, cy, size, size)
        origin = pyray.Vector2(size / 2, size / 2)
        pyray.draw_texture_pro(sheet, src, dst, origin, 0.0, pyray.WHITE)

    def _ghost_row(self, ghost: Ghost) -> int:
        if ghost.is_edible:
            if (self.engine.frightened_remaining < FLASH_AT
                    and (self.frame // 6) % 2 == 0):
                return FRIGHTENED_FLASH_ROW
            return FRIGHTENED_ROW
        return GHOST_BASE_ROW[ghost.kind] + DIR_OFFSET.get(ghost.direction, 0)

    def _wall_line(self, x0, y0, x1, y1, t) -> None:
        s = self.window_handler.to_screen
        pyray.draw_line_ex(
            pyray.Vector2(s(x0), s(y0)), pyray.Vector2(s(x1), s(y1)),
            s(t), WALL_COLOR)

    def _draw_walls(self, board, x, y, cell, t) -> None:
        s = self.window_handler.to_screen
        x1, y1 = x + cell, y + cell
        if board.walls & Direction.NORTH:
            self._wall_line(x, y, x1, y, t)
        if board.walls & Direction.SOUTH:
            self._wall_line(x, y1, x1, y1, t)
        if board.walls & Direction.WEST:
            self._wall_line(x, y, x, y1, t)
        if board.walls & Direction.EAST:
            self._wall_line(x1, y, x1, y1, t)
        corners = (
            (x, y, Direction.NORTH | Direction.WEST),
            (x1, y, Direction.NORTH | Direction.EAST),
            (x, y1, Direction.SOUTH | Direction.WEST),
            (x1, y1, Direction.SOUTH | Direction.EAST),
        )
        for px, py, mask in corners:
            if board.walls & mask:
                pyray.draw_circle(s(px), s(py), s(t) / 2, WALL_COLOR)

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
        half = cell // 2

        # MAP
        for row in range(rows):
            for col in range(cols):
                board = game_map.game_map[row][col]
                x, y = ox + col * cell, oy + row * cell
                self._draw_walls(board, x, y, cell, thick)
                if board.content is not None:
                    if isinstance(board.content, SuperGum):
                        if self.frame < _FRAMES_ANIMATION // 2:
                            pyray.draw_circle(
                                to_screen(x + half), to_screen(y + half),
                                to_screen(int(cell * 0.28)), GUM_COLOR)
                    else:
                        pyray.draw_circle(
                            to_screen(x + half), to_screen(y + half),
                            to_screen(max(1, int(cell * 0.13))), GUM_COLOR)

        # PACMAN
        pac = self.engine.pacman
        prow, pcol = self.engine.smooth_position(
            pac, self.engine.pacman_progress)
        pcx = ox + int(pcol * cell) + half
        pcy = oy + int(prow * cell) + half
        if pac.prev == pac.position:
            step = 0
        else:
            step = _CHOMP[(self.frame // 4) % len(_CHOMP)]
        index = PAC_FRAMES[pac.direction][step]
        self._draw_sprite(
            self.pac_sheet, index % PAC_COLS, index // PAC_COLS,
            to_screen(pcx), to_screen(pcy), to_screen(cell) * SPRITE_SCALE)

        # GHOSTS
        anim = (self.frame // 8) % 2
        for ghost in self.engine.ghosts:
            grow, gcol = self.engine.smooth_position(
                ghost, self.engine.ghost_progress)
            gx = ox + int(gcol * cell) + half
            gy = oy + int(grow * cell) + half
            self._draw_sprite(
                self.ghost_sheet, anim, self._ghost_row(ghost),
                to_screen(gx), to_screen(gy), to_screen(cell) * SPRITE_SCALE)

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

        if self.frame == _FRAMES_ANIMATION:
            self.frame = 0
        else:
            self.frame += 1
