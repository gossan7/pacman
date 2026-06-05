from typing import Any

from .engine import Engine
from ..state import GlobalState
from ..state import EngineFlag


class ScoreEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.SCORE

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
