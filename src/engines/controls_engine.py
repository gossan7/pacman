from typing import Any

from . import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


CONTROLS = [
    ("UP", "[W]  |  [UP KEY]"),
    ("DOWN", "[S]  |  [DOWN KEY]"),
    ("LEFT", "[A]  |  [LEFT KEY]"),
    ("RIGHT", "[D]  |  [RIGHT KEY]"),
    ("QUIT", "[ESC]"),
    ("OK", "[ENTER]")
]


class ControlsEngine(PopupEngine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.CONTROLS
        self.controls = CONTROLS

    def update_focus(self, globalstate: GlobalState) -> None:
        super().update_focus(globalstate)
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.ESCAPE:
                    globalstate.to_remove = 1
