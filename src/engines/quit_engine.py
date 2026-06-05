from .popup_engine import RegionPopupEngine


REGIONS = [
    "YES"
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
        return
