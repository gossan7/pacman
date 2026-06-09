from typing import Any

from .engine import Engine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


SCORES = [
    ("Feur", 67),
    ("Baka", 1337),
    ("Gravier Miel", 42)
]


class ScoresEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.SCORES
        self.scores = SCORES

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.ESCAPE:
                    globalstate.to_remove = 1
