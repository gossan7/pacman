from typing import Any
import pyray

from .popup_renderer import PopupRenderer, POPUP_WIDTH, POPUP_HEIGHT
from ..engines import ScoresEngine
from .window_handler import WindowHandler


TEXT_ABOVE = "SCORES"
TEXT_SIZE_ABOVE = 50
TEXT_SIZE = 20
TEXT_PADDING = 10


class ScoresRenderer(PopupRenderer):
    def __init__(
        self,
        config: dict[str, Any],
        engine: ScoresEngine,
        window_handler: WindowHandler
    ) -> None:
        super().__init__(config, engine, window_handler)
        self.engine: ScoresEngine = engine

    def _centered_x(self, text: str, font_size: int) -> int:
        to_screen = self.window_handler.to_screen
        text_width = pyray.measure_text(text, to_screen(font_size))
        return to_screen(self.popup_x) + (to_screen(POPUP_WIDTH) - text_width) // 2

    def render(self) -> None:
        super().render()
        to_screen = self.window_handler.to_screen
        n = len(self.engine.scores)
        content_height = TEXT_SIZE_ABOVE + TEXT_PADDING + n * (TEXT_SIZE + TEXT_PADDING)
        start_y = self.popup_y + (POPUP_HEIGHT - content_height) // 2
        pyray.draw_text(
            TEXT_ABOVE,
            self._centered_x(TEXT_ABOVE, TEXT_SIZE_ABOVE),
            to_screen(start_y),
            to_screen(TEXT_SIZE_ABOVE),
            pyray.YELLOW
        )
        for i, (name, score) in enumerate(self.engine.scores):
            full_text = f"{name} - {score}"
            left = f"{name} - "
            y = to_screen(start_y + TEXT_SIZE_ABOVE + TEXT_PADDING * 2 + i * (TEXT_SIZE + TEXT_PADDING))
            x = self._centered_x(full_text, TEXT_SIZE)
            font_size = to_screen(TEXT_SIZE)
            pyray.draw_text(left, x, y, font_size, pyray.WHITE)
            pyray.draw_text(
                str(score),
                x + pyray.measure_text(left, font_size),
                y,
                font_size,
                pyray.YELLOW
            )
