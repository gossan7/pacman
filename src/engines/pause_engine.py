from .engine import Engine
from .global_state import GlobalState
from .engine_flag import EngineFlag


class PauseEngine(Engine):
    def __init__(self, is_running: bool = True,
                 is_listening: bool = True) -> None:
        super().__init__(is_running, is_listening)
        self.EngineFlag = EngineFlag.PAUSE

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
