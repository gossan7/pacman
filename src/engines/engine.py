from typing import Any
from abc import ABC, abstractmethod

from ..state import GlobalState
from ..state import EngineFlag


class Engine(ABC):
    def __init__(self, config: dict[str, Any]) -> None:
        self.flag = EngineFlag.NONE
        self.config = config

    @abstractmethod
    def update_always(self, globalstate: GlobalState) -> None:
        pass

    @abstractmethod
    def update_focus(self, globalstate: GlobalState) -> None:
        pass

    def update(self, globalstate: GlobalState) -> None:
        self.update_always(globalstate)
        if globalstate.focus == self.flag:
            self.update_focus(globalstate)
