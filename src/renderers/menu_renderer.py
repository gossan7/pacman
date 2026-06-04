from typing import Any
import pyray

from .renderer import Renderer
from ..engines import MenuEngine
from .window_handler import WindowHandler, WORLD_WIDTH, WORLD_HEIGHT
from ..engines.menu_engine import REGIONS, REGIONS_STR


REGION_HEIGHT = 50
REGION_PADDING = 20
BORDER_SIZE = 200
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
        # pyray.draw_text("Pacman", 100, 10, 20, pyray.WHITE)
        region_width = WORLD_WIDTH - BORDER_SIZE * 2 - REGION_PADDING * 2
        for i, region in enumerate(REGIONS):
            y = 100 + i * REGION_HEIGHT + i * REGION_PADDING

            pyray.draw_rectangle(
                to_screen(BORDER_SIZE + REGION_PADDING),
                to_screen(y),
                to_screen(region_width),
                to_screen(REGION_HEIGHT),
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

                pyray.draw_text(
                    REGIONS_STR[region],
                    to_screen(
                        BORDER_SIZE +
                        REGION_PADDING +
                        OUTER_LINE_SIZE *
                        2
                    ),
                    to_screen(
                        y +
                        OUTER_LINE_SIZE *
                        2
                    ),
                    to_screen(20),
                    pyray.WHITE
                )
            else:
                pyray.draw_text(
                    REGIONS_STR[region],
                    to_screen(
                        BORDER_SIZE +
                        REGION_PADDING +
                        OUTER_LINE_SIZE *
                        2
                    ),
                    to_screen(
                        y +
                        OUTER_LINE_SIZE *
                        2
                    ),
                    to_screen(20),
                    pyray.BLACK
                )
