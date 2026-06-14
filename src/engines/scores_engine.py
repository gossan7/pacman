from typing import Any

from .popup_engine import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


SCORES = [
    ("Feur", 67),
    ("Baka", 1337),
    ("Gravier Miel", 42)
]


class ScoresEngine(PopupEngine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.SCORES
        self.scores = SCORES

    def update_focus(self, globalstate: GlobalState) -> None:
        super().update_focus(globalstate)
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.ESCAPE:
                    globalstate.to_remove = 1
