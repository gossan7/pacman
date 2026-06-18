from typing import Any
import pyray

from .renderer import Renderer
from ..engines import PopupEngine
from .window_handler import WindowHandler, WORLD_WIDTH, WORLD_HEIGHT


OVERLAY_ALPHA = 150
POPUP_WIDTH = WORLD_WIDTH // 2
POPUP_HEIGHT = WORLD_HEIGHT // 2
OUTER_LINE_SIZE = 5


class PopupRenderer(Renderer):
    """
    Base renderer that draws a centred popup panel.

    Dims the screen behind the first popup and draws the bordered panel;
    subclasses call ``super().render()`` and then draw their contents on
    top.
    """

    def __init__(
            self,
            config: dict[str, Any],
            engine: PopupEngine,
            window_handler: WindowHandler
    ) -> None:
        """
        Store the dependencies and compute the centred panel origin.

        Args:
            config: Validated configuration dict.
            engine: The popup engine being drawn.
            window_handler: Helper for world-to-screen scaling.
        """
        self.config = config
        self.engine: PopupEngine = engine
        self.window_handler = window_handler
        self.popup_x = (WORLD_WIDTH - POPUP_WIDTH) // 2
        self.popup_y = (WORLD_HEIGHT - POPUP_HEIGHT) // 2

    def render(self) -> None:
        """
        Draw the dim overlay (for the first popup) and the bordered panel.
        """
        to_screen = self.window_handler.to_screen

        if self.engine.popup == 1:
            pyray.draw_rectangle(
                0, 0,
                to_screen(WORLD_WIDTH), to_screen(WORLD_HEIGHT),
                pyray.Color(0, 0, 0, OVERLAY_ALPHA)
            )

        pyray.draw_rectangle(
            to_screen(self.popup_x),
            to_screen(self.popup_y),
            to_screen(POPUP_WIDTH),
            to_screen(POPUP_HEIGHT),
            pyray.WHITE
        )

        pyray.draw_rectangle(
            to_screen(self.popup_x + OUTER_LINE_SIZE),
            to_screen(self.popup_y + OUTER_LINE_SIZE),
            to_screen(POPUP_WIDTH - OUTER_LINE_SIZE * 2),
            to_screen(POPUP_HEIGHT - OUTER_LINE_SIZE * 2),
            pyray.BLACK
        )
