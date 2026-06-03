from .renderer import Renderer
from ..engines import Engine


class CheatRenderer(Renderer):
    def __init__(self, config: dict, engine: Engine) -> None:
        super().__init__(config, engine)

    def render(self):
        pass
