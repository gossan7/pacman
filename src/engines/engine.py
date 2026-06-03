from abc import ABC, abstractmethod
from ..state import GlobalState
from ..state import EngineFlag


class Engine(ABC):
    def __init__(self) -> None:
        self.flag = EngineFlag.NONE

    @abstractmethod
    def update_always(self, globalstate: GlobalState, controls: dict) -> None:
        pass

    @abstractmethod
    def update_focus(self, globalstate: GlobalState, controls: dict) -> None:
        pass

    def update(self, globalstate: GlobalState, controls: dict) -> None:
        self.update_always(globalstate, controls)
        if globalstate.focus == self.flag:
            self.update_focus(globalstate, controls)
