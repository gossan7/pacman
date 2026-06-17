from typing import Any

from .popup_engine import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


class ScoresEngine(PopupEngine):
    """
    Popup that displays the highscore table.

    Mirrors the current scores from the shared state and closes on escape.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the scores popup with an empty cache.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.flag = EngineFlag.SCORES
        self.scores: list[tuple[str, int]] = []

    def update_always(self, globalstate: GlobalState) -> None:
        """
        Refresh the cached scores from the shared state.

        Args:
            globalstate: The shared mutable game state.
        """
        super().update_always(globalstate)
        self.scores = globalstate.scores

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
