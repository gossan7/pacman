from typing import Any

from .renderer import Renderer
from ..engines import Engine


class GameRenderer(Renderer):
    def __init__(self, config: dict[str, Any], engine: Engine) -> None:
        super().__init__(config, engine)

    def render(self) -> None:
        pass
