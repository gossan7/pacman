from typing import Any
from abc import ABC, abstractmethod

from ..engines import Engine
from .window_handler import WindowHandler


class Renderer(ABC):
    def __init__(
        self,
        config: dict[str, Any],
        engine: Engine,
        window_handler: WindowHandler
    ) -> None:
        self.config = config
        self.engine = engine
        self.window_handler = window_handler

    @abstractmethod
    def render(self) -> None:
        pass
