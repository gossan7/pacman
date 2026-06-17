from typing import Any
import pyray

from . import PopupRenderer
from ..engines import RegionPopupEngine
from .window_handler import WindowHandler, WORLD_WIDTH, WORLD_HEIGHT


OVERLAY_ALPHA = 150
TEXT_SIZE_ABOVE = 50
TEXT_POPUP_GAP = 20
POPUP_WIDTH = WORLD_WIDTH // 2
POPUP_HEIGHT = WORLD_HEIGHT // 2
POPUP_PADDING = 20
REGION_HEIGHT = 45
REGION_PADDING = 10
FONT_SIZE = 15
OUTER_LINE_SIZE = 5
TOGGLE_OUTER_LINE = 2

TOGGLE_WIDTH = 40
TOGGLE_HEIGHT = 20
TOGGLE_PAD = 5


class RegionPopupRenderer(PopupRenderer):
    def __init__(
            self,
            config: dict[str, Any],
            engine: RegionPopupEngine,
            window_handler: WindowHandler
    ) -> None:
        super().__init__(config, engine, window_handler)
        self.config = config
        self.engine: RegionPopupEngine = engine
        self.window_handler = window_handler

    def _draw_toggle(
            self,
            rx: int,
            ry: int,
            rw: int,
            rh: int,
            on: bool,
            hover_on: bool
    ) -> None:
        to_screen = self.window_handler.to_screen
        sw = to_screen(TOGGLE_WIDTH)
        sh = to_screen(TOGGLE_HEIGHT)
        sx = rx + rw - to_screen(REGION_PADDING) - sw
        sy = ry + (rh - sh) // 2

        outer_color = pyray.BLACK if hover_on else pyray.WHITE
        inner_color = pyray.WHITE if hover_on else pyray.BLACK

        pyray.draw_rectangle(sx, sy, sw, sh, outer_color)
        decay = to_screen(TOGGLE_OUTER_LINE)

        pyray.draw_rectangle(
            sx + decay,
            sy + decay,
            sw - decay * 2,
            sh - decay * 2,
            inner_color
        )

        tsize = sh - to_screen(TOGGLE_PAD) * 2
        ty = sy + to_screen(TOGGLE_PAD)
        tx = sx + sw - tsize - to_screen(TOGGLE_PAD) if on \
            else sx + to_screen(TOGGLE_PAD)

        if hover_on:
            track = pyray.BLACK
        elif on:
            track = pyray.YELLOW
        else:
            track = pyray.WHITE

        pyray.draw_rectangle(tx, ty, tsize, tsize, track)

    def render(self) -> None:
        super().render()
        to_screen = self.window_handler.to_screen

        n = len(self.engine.regions)

        regions_block_height = n * REGION_HEIGHT + \
            max(n - 1, 0) * REGION_PADDING
        content_height = TEXT_SIZE_ABOVE + TEXT_POPUP_GAP \
            + regions_block_height

        block_top = self.popup_y + (POPUP_HEIGHT - content_height) // 2

        font_size_above = to_screen(TEXT_SIZE_ABOVE)
        text_width = pyray.measure_text(
            self.engine.text_to_display, font_size_above
        )
        text_x = (to_screen(WORLD_WIDTH) - text_width) // 2

        pyray.draw_text(
            self.engine.text_to_display,
            text_x, to_screen(block_top),
            font_size_above,
            pyray.YELLOW
        )

        font_size = to_screen(FONT_SIZE)
        region_width = POPUP_WIDTH - POPUP_PADDING * 2
        region_x = self.popup_x + POPUP_PADDING
        regions_start_y = block_top + TEXT_SIZE_ABOVE + TEXT_POPUP_GAP

        for i, region_text in enumerate(self.engine.regions):
            y = regions_start_y + i * (REGION_HEIGHT + REGION_PADDING)

            rect_screen_x = to_screen(region_x)
            rect_screen_y = to_screen(y)
            rect_screen_width = to_screen(region_width)
            rect_screen_height = to_screen(REGION_HEIGHT)

            item_text_width = pyray.measure_text(region_text, font_size)
            item_text_x = rect_screen_x + \
                (rect_screen_width - item_text_width) // 2
            item_text_y = rect_screen_y + (rect_screen_height - font_size) // 2

            pyray.draw_rectangle(
                rect_screen_x, rect_screen_y,
                rect_screen_width, rect_screen_height,
                pyray.WHITE
            )

            if i != self.engine.hover_on:
                pyray.draw_rectangle(
                    to_screen(region_x + OUTER_LINE_SIZE),
                    to_screen(y + OUTER_LINE_SIZE),
                    to_screen(region_width - OUTER_LINE_SIZE * 2),
                    to_screen(REGION_HEIGHT - OUTER_LINE_SIZE * 2),
                    pyray.BLACK
                )
                pyray.draw_text(
                    region_text,
                    item_text_x,
                    item_text_y,
                    font_size,
                    pyray.WHITE
                )
            else:
                pyray.draw_text(
                    region_text,
                    item_text_x,
                    item_text_y,
                    font_size,
                    pyray.BLACK
                )
            status = self.engine.region_status(i)
            if status is not None:
                self._draw_toggle(
                    rect_screen_x, rect_screen_y,
                    rect_screen_width, rect_screen_height,
                    status == "ON",
                    self.engine.hover_on == i
                )
