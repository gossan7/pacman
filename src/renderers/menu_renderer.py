from typing import Any
import pyray

from .renderer import Renderer
from ..engines import MenuEngine
from .window_handler import WindowHandler, WORLD_WIDTH
from ..engines.menu_engine import REGIONS


GAME_NAME = "PACMAN"
GAME_NAME_SIZE = 150
REGION_HEIGHT = 50
REGION_PADDING = 20
FONT_SIZE = 20
BORDER_SIZE = 250
OUTER_LINE_SIZE = 5


class MenuRenderer(Renderer):
    def __init__(
            self,
            config: dict[str, Any],
            engine: MenuEngine,
            window_handler: WindowHandler
    ) -> None:
        self.config = config
        self.engine: MenuEngine = engine
        self.window_handler = window_handler

    def render(self) -> None:
        to_screen = self.window_handler.to_screen
        pyray.clear_background(pyray.BLACK)

        text_width = pyray.measure_text(GAME_NAME, to_screen(GAME_NAME_SIZE))
        text_x = (to_screen(WORLD_WIDTH) - text_width) // 2
        text_y = (to_screen(GAME_NAME_SIZE + REGION_PADDING * 2) -
                  to_screen(GAME_NAME_SIZE)) // 2

        pyray.draw_text(
            "PACMAN",
            text_x,
            text_y,
            to_screen(GAME_NAME_SIZE),
            pyray.YELLOW
        )

        region_width = WORLD_WIDTH - BORDER_SIZE * 2 - REGION_PADDING * 2
        font_size = to_screen(FONT_SIZE)
        for i, region in enumerate(REGIONS):
            y = GAME_NAME_SIZE + REGION_PADDING * 2 + \
                i * (REGION_HEIGHT + REGION_PADDING)

            text_width = pyray.measure_text(region, font_size)
            rect_screen_x = to_screen(BORDER_SIZE + REGION_PADDING)
            rect_screen_width = to_screen(region_width)
            rect_screen_height = to_screen(REGION_HEIGHT)

            text_x = rect_screen_x + (rect_screen_width - text_width) // 2
            text_y = to_screen(y) + (rect_screen_height - font_size) // 2

            pyray.draw_rectangle(
                rect_screen_x,
                to_screen(y),
                rect_screen_width,
                rect_screen_height,
                pyray.WHITE
            )

            if i != self.engine.hover_on:
                pyray.draw_rectangle(
                    to_screen(BORDER_SIZE + REGION_PADDING + OUTER_LINE_SIZE),
                    to_screen(y + OUTER_LINE_SIZE),
                    to_screen(region_width - OUTER_LINE_SIZE * 2),
                    to_screen(REGION_HEIGHT - OUTER_LINE_SIZE * 2),
                    pyray.BLACK
                )
                pyray.draw_text(region, text_x, text_y, font_size, pyray.WHITE)
            else:
                pyray.draw_text(region, text_x, text_y, font_size, pyray.BLACK)
