from typing import Any

from .region_popup_engine import RegionPopupEngine
from ..state import GlobalState
from ..state import EngineFlag

REGIONS = [
    "INVICIBILITY",
    "GHOST FREEZE",
    "INCREASED SPEED",
    "EXTRA LIFE",
    "WIN LEVEL"
]

ACTIONS = {
    "INVICIBILITY": "invincibility",
    "GHOST FREEZE": "ghost_freeze",
    "INCREASED SPEED": "increased_speed",
    "EXTRA LIFE": "extra_life",
    "WIN LEVEL": "win_level"
}

TEXT_TO_DISPLAY = "CHEATS"


class CheatEngine(RegionPopupEngine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.CHEAT
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY

    def activate_current_hover(self, globalstate: GlobalState) -> None:
        cheat = ACTIONS[REGIONS[self.hover_on]]
        globalstate.cheats_state[cheat] = not globalstate.cheats_state[cheat]
