from typing import Any
import pyray

from .renderer import Renderer
from ..engines import MenuEngine
from ..engines.menu_engine import REGIONS, REGIONS_STR

REGION_SIZE = (200, 50)
REGION_PADDING = 20


class MenuRenderer(Renderer):
    def __init__(self, config: dict[str, Any], engine: MenuEngine) -> None:
        self.config = config
        self.engine: MenuEngine = engine

    def render(self) -> None:
        pyray.clear_background(pyray.BLACK)
        pyray.draw_text("Pacman", 100, 10, 20, pyray.WHITE)
        for i, region in enumerate(REGIONS):
            y = 100 + i * REGION_SIZE[1] + i * REGION_PADDING

            pyray.draw_rectangle(
                100,
                y,
                REGION_SIZE[0],
                REGION_SIZE[1],
                pyray.WHITE
            )

            if i != self.engine.hover_on:
                pyray.draw_rectangle(
                    105,
                    y + 5,
                    REGION_SIZE[0] - 10,
                    REGION_SIZE[1] - 10,
                    pyray.BLACK
                )
                pyray.draw_text(
                    REGIONS_STR[region],
                    110,
                    y + 10,
                    20,
                    pyray.WHITE
                )
            else:
                pyray.draw_text(
                    REGIONS_STR[region],
                    110,
                    y + 10,
                    20,
                    pyray.BLACK
                )
