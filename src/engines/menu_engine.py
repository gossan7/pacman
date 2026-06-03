from .engine import Engine
from ..state import GlobalState
from ..state import EngineFlag


class MenuEngine(Engine):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.flag = EngineFlag.MENU

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
