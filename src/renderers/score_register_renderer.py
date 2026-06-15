from typing import Any
import pyray

from .popup_renderer import PopupRenderer, POPUP_WIDTH, POPUP_HEIGHT
from ..engines import ScoreRegisterEngine
from .window_handler import WindowHandler


TITLE_WON = "YOU WIN!"
TITLE_LOST = "GAME OVER"
PROMPT = "ENTER YOUR NAME:"
TITLE_SIZE = 50
TEXT_SIZE = 24
PADDING = 14


class ScoreRegisterRenderer(PopupRenderer):
    def __init__(
        self,
        config: dict[str, Any],
        engine: ScoreRegisterEngine,
        window_handler: WindowHandler
    ) -> None:
        super().__init__(config, engine, window_handler)
        self.engine: ScoreRegisterEngine = engine

    def _centered_x(self, text: str, font_size: int) -> int:
        to_screen = self.window_handler.to_screen
        text_width = pyray.measure_text(text, to_screen(font_size))
        return to_screen(self.popup_x) + \
            (to_screen(POPUP_WIDTH) - text_width) // 2

    def render(self) -> None:
        super().render()
        to_screen = self.window_handler.to_screen
        title = TITLE_WON if self.engine.won else TITLE_LOST
        score_text = f"SCORE: {self.engine.score}"
        name_text = f"{self.engine.name}_"

        lines = [
            (title, TITLE_SIZE, pyray.YELLOW),
            (score_text, TEXT_SIZE, pyray.WHITE),
            (PROMPT, TEXT_SIZE, pyray.WHITE),
            (name_text, TEXT_SIZE, pyray.YELLOW),
        ]
        content_height = sum(size for _, size, _ in lines) + \
            PADDING * (len(lines) - 1)
        y = self.popup_y + (POPUP_HEIGHT - content_height) // 2

        for text, size, color in lines:
            pyray.draw_text(
                text,
                self._centered_x(text, size),
                to_screen(y),
                to_screen(size),
                color
            )
            y += size + PADDING
