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
    """
    Popup that lists the keyboard controls.

    Purely informational; closes on escape.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the controls popup with the key bindings to show.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.flag = EngineFlag.CONTROLS
        self.controls = CONTROLS

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Close the popup when escape is pressed.

        Args:
            globalstate: The shared mutable game state.
        """
        super().update_focus(globalstate)
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.ESCAPE:
                    globalstate.to_remove = 1
