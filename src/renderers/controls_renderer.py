from typing import Any
import pyray

from .popup_renderer import PopupRenderer, POPUP_WIDTH, POPUP_HEIGHT
from ..engines import ControlsEngine
from .window_handler import WindowHandler


TEXT_ABOVE = "CONTROLS"
TEXT_SIZE_ABOVE = 50
TEXT_SIZE = 20
TEXT_PADDING = 10


class ControlsRenderer(PopupRenderer):
    def __init__(
        self,
        config: dict[str, Any],
        engine: ControlsEngine,
        window_handler: WindowHandler
    ) -> None:
        super().__init__(config, engine, window_handler)
        self.engine: ControlsEngine = engine

    def _centered_x(self, text: str, font_size: int) -> int:
        to_screen = self.window_handler.to_screen
        text_width = pyray.measure_text(text, to_screen(font_size))
        return to_screen(self.popup_x) + \
            (to_screen(POPUP_WIDTH) - text_width) // 2

    def render(self) -> None:
        super().render()
        to_screen = self.window_handler.to_screen
        n = len(self.engine.controls)
        content_height = TEXT_SIZE_ABOVE + \
            TEXT_PADDING + n * (TEXT_SIZE + TEXT_PADDING)
        start_y = self.popup_y + (POPUP_HEIGHT - content_height) // 2
        pyray.draw_text(
            TEXT_ABOVE,
            self._centered_x(TEXT_ABOVE, TEXT_SIZE_ABOVE),
            to_screen(start_y),
            to_screen(TEXT_SIZE_ABOVE),
            pyray.YELLOW
        )
        for i, (action, key) in enumerate(self.engine.controls):
            full_text = f"{action} - {key}"
            y = to_screen(start_y + TEXT_SIZE_ABOVE +
                          TEXT_PADDING * 2 + i * (TEXT_SIZE + TEXT_PADDING))
            font_size = to_screen(TEXT_SIZE)
            cursor_x = self._centered_x(full_text, TEXT_SIZE)
            parts = [(f"{action} - ", pyray.WHITE)]
            if " | " in key:
                left_key, right_key = key.split(" | ", 1)
                parts += [(left_key, pyray.YELLOW),
                          (" | ", pyray.WHITE), (right_key, pyray.YELLOW)]
            else:
                parts.append((key, pyray.YELLOW))
            for segment, color in parts:
                pyray.draw_text(segment, cursor_x, y, font_size, color)
                cursor_x += pyray.measure_text(segment, font_size)
