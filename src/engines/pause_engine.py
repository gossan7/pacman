from .popup_engine import RegionPopupEngine
from ..state import EngineFlag


REGIONS = [
    "RESUME",
    "OPTIONS",
    "QUIT"
]

ACTIONS = {
    "RESUME": (None, 1),
    "OPTIONS": (EngineFlag.OPTIONS, 0),
    "QUIT": (EngineFlag.QUIT, 0)
}

TEXT_TO_DISPLAY = "PAUSE"


class PauseEngine(RegionPopupEngine):
    def __init__(self, config):
        super().__init__(config)
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY

    def activate_current_hover(self, globalstate):
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        if REGIONS[self.hover_on] == "QUIT":
            to_remove = globalstate.to_quit = 3
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add
