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
REGION_HEIGHT = 50
REGION_PADDING = 10
FONT_SIZE = 20
OUTER_LINE_SIZE = 5


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

    def render(self) -> None:
        super().render()
        to_screen = self.window_handler.to_screen

        start_y = (WORLD_HEIGHT - POPUP_HEIGHT) // 2
        font_size_above = to_screen(TEXT_SIZE_ABOVE)
        text_width = pyray.measure_text(
            self.engine.text_to_display, font_size_above
        )
        text_x = (to_screen(WORLD_WIDTH) - text_width) // 2

        pyray.draw_text(
            self.engine.text_to_display,
            text_x, to_screen(start_y + TEXT_POPUP_GAP),
            font_size_above,
            pyray.YELLOW
        )

        font_size = to_screen(FONT_SIZE)
        region_width = POPUP_WIDTH - POPUP_PADDING * 2
        region_x = self.popup_x + POPUP_PADDING

        for i, region_text in enumerate(self.engine.regions):
            y = TEXT_SIZE_ABOVE + TEXT_POPUP_GAP * 2 + self.popup_y + \
                i * (REGION_HEIGHT + REGION_PADDING)

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
