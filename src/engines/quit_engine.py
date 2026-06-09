from .popup_engine import RegionPopupEngine


REGIONS = [
    "YES",
    "NO"
]

ACTIONS = {
    "YES": (None, 2),
    "NO": (None, 1)
}

TEXT_TO_DISPLAY = "QUIT ?"


class QuitEngine(RegionPopupEngine):
    def __init__(self, config):
        super().__init__(config)
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY

    def activate_current_hover(self, globalstate):
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        if REGIONS[self.hover_on] == "YES":
            to_remove = globalstate.to_quit
            to_add = globalstate.to_add_on_quit
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add
