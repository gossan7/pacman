from typing import Any

from .popup_engine import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


class ScoresEngine(PopupEngine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.SCORES
        self.scores: list[tuple[str, int]] = []

    def update_always(self, globalstate: GlobalState) -> None:
        super().update_always(globalstate)
        self.scores = globalstate.scores

    def update_focus(self, globalstate: GlobalState) -> None:
        super().update_focus(globalstate)
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.ESCAPE:
                    globalstate.to_remove = 1
