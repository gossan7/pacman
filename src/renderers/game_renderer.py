from __future__ import annotations

from typing import Any
import pyray

from .renderer import Renderer
from ..engines import GameEngine
from .window_handler import WindowHandler, WORLD_WIDTH, WORLD_HEIGHT
from ..instances import Direction, SuperGum, Ghost
from ..state import GhostKind, GhostMode


HUD_HEIGHT = 90
MARGIN = 20
HUD_FONT = 36

PACMAN_SHEET = str("assets/pacman.png")
GHOSTS_SHEET = str("assets/ghosts.png")

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
EYE_FRAMES = {
    Direction.NORTH: (1, 17),
    Direction.SOUTH: (0, 16),
    Direction.WEST: (1, 16),
    Direction.EAST: (0, 17),
}
DIR_OFFSET = {
    Direction.SOUTH: 0,
    Direction.WEST: 1,
    Direction.EAST: 2,
    Direction.NORTH: 3,
}
DEATH_FRAMES = (9, 10, 11, 12, 13, 14, 15, 16, 17, 18)

FRIGHTENED_ROW = 18
FRIGHTENED_FLASH_ROW = 19
FLASH_AT = 2.0

_FRAMES_ANIMATION = 30

_TURNS = ({"U", "D"}, {"L", "R"})


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
        self._maze_tex: Any = None
        self._created_map: Any = None
        self._tex_dimensions: tuple[int, int] | None = None

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
        if self._maze_tex is not None:
            pyray.unload_render_texture(self._maze_tex)

    # MAP CREATORS

    def _wall(self, r: int, c: int, bit: Direction) -> bool:
        m = self.engine.map
        if r < 0 or c < 0 or r >= m.height or c >= m.width:
            return False
        return bool(m.game_map[r][c].walls & bit)

    def _segments(self, vr: int, vc: int) -> set:
        seg = set()
        if self._wall(vr - 1, vc, Direction.WEST) \
                or self._wall(vr - 1, vc - 1, Direction.EAST):
            seg.add("U")
        if self._wall(vr, vc, Direction.WEST) \
                or self._wall(vr, vc - 1, Direction.EAST):
            seg.add("D")
        if self._wall(vr, vc - 1, Direction.NORTH) \
                or self._wall(vr - 1, vc - 1, Direction.SOUTH):
            seg.add("L")
        if self._wall(vr, vc, Direction.NORTH) \
                or self._wall(vr - 1, vc, Direction.SOUTH):
            seg.add("R")
        return seg

    def _is_turn(self, vr: int, vc: int) -> bool:
        seg = self._segments(vr, vc)
        return len(seg) == 2 and seg not in _TURNS

    def _create_walls(self, cell: int, thick: int, ox: int, oy: int) -> None:
        s = self.window_handler.to_ratio
        r = max(thick, cell / 3)
        sr, st = s(r), s(thick)
        rows, cols = self.engine.map.height, self.engine.map.width
        pyray.begin_texture_mode(self._maze_tex)
        pyray.clear_background(pyray.BLANK)
        for vr in range(rows + 1):
            for vc in range(cols):
                if "R" not in self._segments(vr, vc):
                    continue
                y = s(oy + vr * cell)
                x0 = s(ox + vc * cell) + (sr if self._is_turn(vr, vc) else 0)
                x1 = s(ox + (vc + 1) * cell) - \
                    (sr if self._is_turn(vr, vc + 1) else 0)
                pyray.draw_line_ex(
                    pyray.Vector2(x0, y), pyray.Vector2(x1, y),
                    st, WALL_COLOR)
        for vr in range(rows):
            for vc in range(cols + 1):
                if "D" not in self._segments(vr, vc):
                    continue
                x = s(ox + vc * cell)
                y0 = s(oy + vr * cell) + (sr if self._is_turn(vr, vc) else 0)
                y1 = s(oy + (vr + 1) * cell) \
                    - (sr if self._is_turn(vr + 1, vc) else 0)
                pyray.draw_line_ex(
                    pyray.Vector2(x, y0), pyray.Vector2(x, y1),
                    st, WALL_COLOR)
        for vr in range(rows + 1):
            for vc in range(cols + 1):
                self._create_vertex(vr, vc, cell, ox, oy, sr, st)
        pyray.end_texture_mode()

    def _create_vertex(self, vr: int, vc: int, cell: int,
                       ox: int, oy: int, sr: int, st: int) -> None:
        s = self.window_handler.to_ratio
        seg = self._segments(vr, vc)
        if not seg:
            return
        sx, sy = s(ox + vc * cell), s(oy + vr * cell)
        if len(seg) == 2 and seg not in _TURNS:
            cx = sx + (sr if "R" in seg else -sr)
            cy = sy + (sr if "D" in seg else -sr)
            center = pyray.Vector2(cx, cy)
            if seg == {"D", "R"}:
                a0, a1 = 180, 270
            elif seg == {"D", "L"}:
                a0, a1 = 270, 360
            elif seg == {"U", "R"}:
                a0, a1 = 90, 180
            else:
                a0, a1 = 0, 90
            pyray.draw_ring(center, sr - st / 2, sr + st / 2, a0, a1,
                            128, WALL_COLOR)

    # ENTITIES

    def _draw_sprite(
            self, sheet: pyray.Texture, col: int, row: int,
            cx: int, cy: int, size: int,
            tint: pyray.Color | None = None) -> None:
        if tint is None:
            tint = pyray.WHITE
        inset = 0.05
        src = pyray.Rectangle(
            col * SPRITE_PX + inset,
            row * SPRITE_PX + inset,
            SPRITE_PX - 2 * inset,
            SPRITE_PX - 2 * inset)
        dst = pyray.Rectangle(cx, cy, size, size)
        origin = pyray.Vector2(size / 2, size / 2)
        pyray.draw_texture_pro(sheet, src, dst, origin, 0.0, tint)

    def _ghost_row(self, ghost: Ghost) -> int:
        if ghost.is_edible:
            if (self.engine.frightened_remaining < FLASH_AT
                    and (self.frame // 6) % 2 == 0):
                return FRIGHTENED_FLASH_ROW
            return FRIGHTENED_ROW
        return GHOST_BASE_ROW[ghost.kind] + DIR_OFFSET.get(ghost.direction, 0)

    def _eyes_frame(self, ghost: Ghost) -> tuple[int, int]:
        dr = ghost.spawn.row - ghost.eyes_from.row
        dc = ghost.spawn.col - ghost.eyes_from.col
        if abs(dr) >= abs(dc):
            facing = Direction.NORTH if dr < 0 else Direction.SOUTH
        else:
            facing = Direction.WEST if dc < 0 else Direction.EAST
        return EYE_FRAMES[facing]

    # RENDER

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
        sprite = to_screen(int(cell * SPRITE_SCALE))

        # WALLS
        w, h = self.window_handler.dimensions
        if self._maze_tex is None or self._tex_dimensions != (w, h):
            if self._maze_tex is not None:
                pyray.unload_render_texture(self._maze_tex)
            self._maze_tex = pyray.load_render_texture(w, h)
            self._tex_dimensions = (w, h)
            self._created_map = None
        if self.engine.map is not self._created_map:
            self._create_walls(cell, thick, ox, oy)
            self._created_map = self.engine.map
        mtex = self._maze_tex.texture
        pyray.draw_texture_rec(
            mtex, pyray.Rectangle(0, 0, mtex.width, -mtex.height),
            pyray.Vector2(0, 0), pyray.WHITE)

        # GUMS
        for row in range(rows):
            for col in range(cols):
                content = game_map.game_map[row][col].content
                if content is None:
                    continue
                cx = to_screen(ox + col * cell + half)
                cy = to_screen(oy + row * cell + half)
                if isinstance(content, SuperGum):
                    if self.frame < _FRAMES_ANIMATION // 2:
                        pyray.draw_circle(
                            cx, cy, to_screen(int(cell * 0.28)), GUM_COLOR)
                else:
                    pyray.draw_circle(
                        cx, cy, to_screen(max(1, int(cell * 0.13))),
                        GUM_COLOR)

        # PACMAN
        over = self.engine.game_ended
        pac = self.engine.pacman
        prow, pcol = self.engine.smooth_position(
            pac, self.engine.pacman_progress)
        pcx = ox + int(pcol * cell) + half
        pcy = oy + int(prow * cell) + half
        death = self.engine.death_fraction()
        if not over:
            if death is not None:
                di = min(len(DEATH_FRAMES) - 1, int(death * len(DEATH_FRAMES)))
                index = DEATH_FRAMES[di]
            elif pac.prev == pac.position:
                index = PAC_FRAMES[pac.direction][2]
            else:
                step = _CHOMP[(self.frame // 4) % len(_CHOMP)]
                index = PAC_FRAMES[pac.direction][step]
            self._draw_sprite(
                self.pac_sheet, index % PAC_COLS, index // PAC_COLS,
                to_screen(pcx), to_screen(pcy), sprite)

        # GHOSTS
        if death is None and not over:
            anim = (self.frame // 8) % 2
            for ghost in self.engine.ghosts:
                grow, gcol = self.engine.ghost_render_position(
                    ghost, self.engine.ghost_progress)
                gx = ox + int(gcol * cell) + half
                gy = oy + int(grow * cell) + half
                tint = pyray.Color(
                    255, 255, 255, self.engine.ghost_alpha(ghost))
                if ghost.mode == GhostMode.EYES:
                    ecol, erow = self._eyes_frame(ghost)
                    self._draw_sprite(
                        self.ghost_sheet, ecol, erow,
                        to_screen(gx), to_screen(gy), sprite, tint)
                else:
                    self._draw_sprite(
                        self.ghost_sheet, anim, self._ghost_row(ghost),
                        to_screen(gx), to_screen(gy), sprite, tint)

        # HUD
        font = to_screen(HUD_FONT)
        engine = self.engine
        if engine.level_remaining < 1000:
            time_displayed = f"{max(0, round(engine.level_remaining, 2))}"
        else:
            time_displayed = "999+"
        if min(engine.level, engine.max_levels) < 999:
            lvl_displayed = f"{min(engine.level, engine.max_levels)}"
        else:
            lvl_displayed = "99+"
        items = [
            f"SCORE {engine.score if engine.score < 1000000 else '999999+'}",
            f"LEVEL {lvl_displayed}",
            f"LIVES {engine.lives if engine.lives < 99 else '99+'}",
            f"TIME {time_displayed}",
        ]
        colw = (WORLD_WIDTH - 2 * MARGIN) // len(items)
        hy = to_screen(MARGIN)
        for i, text in enumerate(items):
            pyray.draw_text(
                text, to_screen(MARGIN + i * colw), hy, font, pyray.WHITE)

        label = self.engine.banner_label()
        if label is not None:
            big = to_screen(HUD_FONT + 12)
            tw = pyray.measure_text(label, big)
            bx = to_screen(WORLD_WIDTH // 2) - tw // 2
            by = to_screen(MARGIN + HUD_FONT + 8)
            pyray.draw_text(label, bx, by, big, pyray.YELLOW)
        if self.frame == _FRAMES_ANIMATION:
            self.frame = 0
        else:
            self.frame += 1
