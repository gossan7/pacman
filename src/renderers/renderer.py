from typing import Dict
from abc import ABC, abstractmethod
from ..engines import Engine


class Renderer(ABC):
    def __init__(self, engine: Engine, config: Dict) -> None:
        self.engine = engine
        self.config = config

    def switch_full_screen(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass
