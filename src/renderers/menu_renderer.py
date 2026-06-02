from typing import Dict
from .renderer import Renderer
from ..engines import Engine


class MenuRenderer(Renderer):
    def __init__(self, engine: Engine, config: Dict) -> None:
        super().__init__(engine, config)

    def render(self):
        pass
