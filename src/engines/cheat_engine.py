from typing import Any

from .region_popup_engine import RegionPopupEngine
from ..state import GlobalState
from ..state import EngineFlag

REGIONS = [
    "INVINCIBILITY",
    "GHOST FREEZE",
    "INCREASED SPEED",
    "EXTRA LIFE",
    "WIN LEVEL"
]

ACTIONS = {
    "INVINCIBILITY": "invincibility",
    "GHOST FREEZE": "ghost_freeze",
    "INCREASED SPEED": "increased_speed",
    "EXTRA LIFE": "extra_life",
    "WIN LEVEL": "win_level"
}

STATUS_CHEATS = {"invincibility", "ghost_freeze", "increased_speed"}

TEXT_TO_DISPLAY = "CHEATS"


class CheatEngine(RegionPopupEngine):
    """
    Cheat menu popup used for evaluation.

    Toggles cheat flags (invincibility, ghost freeze, increased speed,
    extra life, win level) on the shared state. Toggle-style cheats expose
    an ON/OFF status next to their entry.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the cheat menu with its regions and title.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.flag = EngineFlag.CHEAT
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY
        self._cheats_state: dict[str, bool] = {}

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Handle navigation and cache the current cheat states.

        Args:
            globalstate: The shared mutable game state.
        """
        super().update_focus(globalstate)
        self._cheats_state = globalstate.cheats_state

    def activate_current_hover(self, globalstate: GlobalState) -> None:
        """
        Toggle the cheat bound to the highlighted region.

        Args:
            globalstate: The shared mutable game state.
        """
        cheat = ACTIONS[REGIONS[self.hover_on]]
        globalstate.cheats_state[cheat] = not globalstate.cheats_state[cheat]

    def region_status(self, index: int) -> str | None:
        """
        Return the ON/OFF status of a toggle cheat.

        Args:
            index: Index of the region in ``self.regions``.

        Returns:
            ``"ON"`` or ``"OFF"`` for toggle cheats, or None for one-shot
            cheats that have no persistent state.
        """
        cheat = ACTIONS[self.regions[index]]
        if cheat not in STATUS_CHEATS:
            return None
        return "ON" if self._cheats_state.get(cheat) else "OFF"
