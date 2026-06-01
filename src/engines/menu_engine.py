from .engine import Engine
from .orchestrator import GlobalState
from .engine_flag import EngineFlag


class MenuEngine(Engine):
    def __init__(self, is_running: bool = True,
                 is_listening: bool = True) -> None:
        super.__init__(is_running, is_listening)
        self.flag = EngineFlag.MENU

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
