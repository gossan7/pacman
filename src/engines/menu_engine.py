from .engine import Engine
from ..state import GlobalState
from ..state import EngineFlag


class MenuEngine(Engine):
    def __init__(self) -> None:
        super().__init__()
        self.flag = EngineFlag.MENU

    def update_always(self, globalstate: GlobalState, controls: dict) -> None:
        pass

    def update_focus(self, globalstate: GlobalState, controls: dict) -> None:
        pass
