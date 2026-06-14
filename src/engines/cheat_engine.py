from typing import Any

from .popup_engine import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag


class CheatEngine(PopupEngine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.CHEAT

    def update_focus(self, globalstate: GlobalState) -> None:
        super().update_focus(globalstate)
