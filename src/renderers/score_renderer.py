from typing import Dict
from .renderer import Renderer
from ..engine import Engine


class ScoreRenderer(Renderer):
    def __init__(self, engine: Engine, config: Dict) -> None:
        super().__init__(engine, config)

    def render(self):
        pass
