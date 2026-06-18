from . import RegionPopupEngine
from ..state import EngineFlag


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
    """
    Yes/No confirmation popup shown before quitting.

    Choosing "NO" simply closes the popup; choosing "YES" tears down the
    whole engine stack and either exits or returns to the menu, depending
    on the pending ``to_add_on_quit`` target.
    """

    def __init__(self, config):
        """
        Initialise the quit confirmation with its regions and title.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.flag = EngineFlag.QUIT
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY

    def activate_current_hover(self, globalstate):
        """
        Confirm or cancel the quit based on the highlighted region.

        Args:
            globalstate: The shared mutable game state.
        """
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        if REGIONS[self.hover_on] == "YES":
            to_remove = len(globalstate.engine_stack)
            to_add = globalstate.to_add_on_quit
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add
