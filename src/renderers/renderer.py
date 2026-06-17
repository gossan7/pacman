from typing import Any
from abc import ABC, abstractmethod

from ..engines import Engine
from .window_handler import WindowHandler


class Renderer(ABC):
    """
    Abstract base class for the renderer paired with each engine.

    A renderer reads state from its engine and draws the corresponding
    screen every frame; the window handler converts world coordinates to
    screen pixels.
    """

    def __init__(
        self,
        config: dict[str, Any],
        engine: Engine,
        window_handler: WindowHandler
    ) -> None:
        """
        Store the config, the engine to draw and the window handler.

        Args:
            config: Validated configuration dict.
            engine: The engine whose state this renderer draws.
            window_handler: Helper for world-to-screen scaling.
        """
        self.config = config
        self.engine = engine
        self.window_handler = window_handler

    @abstractmethod
    def render(self) -> None:
        """
        Draw the current frame for the associated engine.
        """
        pass
