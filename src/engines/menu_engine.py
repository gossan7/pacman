from typing import Any

from .engine import Engine
from ..state import GlobalState, EngineFlag, EventsEnum


REGIONS = [
    "PLAY",
    "SCORES",
    "CONTROLS",
    "QUIT"
]

ACTIONS = {
    "PLAY": (EngineFlag.GAME, 1),
    "SCORES": (EngineFlag.SCORES, 0),
    "CONTROLS": (EngineFlag.CONTROLS, 0),
    "QUIT": (EngineFlag.QUIT, 0)
}


class MenuEngine(Engine):
    """
    The main menu screen.

    Lets the player move through the Play / Scores / Controls / Quit
    entries and pushes the matching engine onto the stack when one is
    chosen.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the menu with the first entry highlighted.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.flag = EngineFlag.MENU
        self.hover_on = 0

    def activate_current_hover(self, globalstate: GlobalState) -> None:
        """
        Apply the action bound to the highlighted menu entry.

        Args:
            globalstate: The shared mutable game state.
        """
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add

    def update_always(self, globalstate: GlobalState) -> None:
        """
        Clear the pending quit target each frame.

        Args:
            globalstate: The shared mutable game state.
        """
        globalstate.to_add_on_quit = None

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Handle menu navigation and selection input.

        Args:
            globalstate: The shared mutable game state.
        """
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.UP:
                    self.hover_on = (self.hover_on - 1) % len(REGIONS)
                case EventsEnum.DOWN:
                    self.hover_on = (self.hover_on + 1) % len(REGIONS)
                case EventsEnum.ENTER:
                    self.activate_current_hover(globalstate)
                case EventsEnum.ESCAPE:
                    globalstate.to_add = EngineFlag.QUIT
