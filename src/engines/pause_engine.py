from .engine import Engine
from .global_state import GlobalState
from .engine_flag import EngineFlag


class PauseEngine(Engine):
    def __init__(self) -> None:
        super().__init__()
        self.flag = EngineFlag.PAUSE

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
