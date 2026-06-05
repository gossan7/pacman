from typing import Any

from .renderer import Renderer
from ..engines import Engine
from .window_handler import WindowHandler


class ScoreRenderer(Renderer):
    def __init__(
        self,
        config: dict[str, Any],
        engine: Engine,
        window_handler: WindowHandler
    ) -> None:
        super().__init__(config, engine, window_handler)

    def render(self) -> None:
        pass
