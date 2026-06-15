from .region_popup_engine import RegionPopupEngine
from ..state import EngineFlag


REGIONS = [
    "RESUME",
    "CONTROLS",
    "QUIT"
]

ACTIONS = {
    "RESUME": (None, 1),
    "CONTROLS": (EngineFlag.CONTROLS, 0),
    "QUIT": (EngineFlag.QUIT, 0)
}

TEXT_TO_DISPLAY = "PAUSE"


class PauseEngine(RegionPopupEngine):
    def __init__(self, config):
        super().__init__(config)
        self.flag = EngineFlag.PAUSE
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY

    def activate_current_hover(self, globalstate):
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        if REGIONS[self.hover_on] == "QUIT":
            globalstate.to_add_on_quit = EngineFlag.MENU
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add
