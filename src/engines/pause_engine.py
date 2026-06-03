from .engine import Engine
from ..state import GlobalState
from ..state import EngineFlag


class PauseEngine(Engine):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.flag = EngineFlag.PAUSE

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
