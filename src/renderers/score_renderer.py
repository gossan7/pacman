from .renderer import Renderer
from ..engines import Engine


class ScoreRenderer(Renderer):
    def __init__(self, engine: Engine, config: dict) -> None:
        super().__init__(engine, config)

    def render(self):
        pass
