from .popup_engine import RegionPopupEngine


REGIONS = [
    "YES",
    "NO"
]

ACTIONS = {
    "YES": (None, 2),
    "NO": (None, 1)
}

TEXT_TO_DISPLAY = "Do you wanna quit ?"


class QuitEngine(RegionPopupEngine):
    def __init__(self, config):
        super().__init__(config)
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY

    def activate_current_hover(self, globalstate):
        to_add, remove = ACTIONS[REGIONS[self.hover_on]]
        globalstate.to_remove += 1 if remove else 0
        if to_add:
            globalstate.to_add = to_add
