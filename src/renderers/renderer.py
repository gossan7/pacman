from abc import ABC, abstractmethod

from ..engines import Engine


class Renderer(ABC):
    def __init__(self, config: dict, engine: Engine) -> None:
        self.config = config
        self.engine = engine

    @abstractmethod
    def render(self) -> None:
        pass
