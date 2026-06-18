from typing import Any
from abc import abstractmethod

from .popup_engine import PopupEngine
from ..state import GlobalState, EventsEnum


class RegionPopupEngine(PopupEngine):
    """
    Base engine for popups offering a vertical list of selectable regions.

    Handles up/down navigation between regions, enter to activate the
    highlighted one and escape to close. Subclasses define the regions and
    what activating each one does.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the region list, hover index and title.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.regions = ["NONE"]
        self.hover_on = 0
        self.text_to_display: str = ""

    @abstractmethod
    def activate_current_hover(self, globalstate: GlobalState) -> None:
        """
        Perform the action bound to the currently highlighted region.

        Args:
            globalstate: The shared mutable game state.
        """
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Handle navigation and activation input while focused.

        Args:
            globalstate: The shared mutable game state.
        """
        super().update_focus(globalstate)
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.UP:
                    self.hover_on = (self.hover_on - 1) % len(self.regions)
                case EventsEnum.DOWN:
                    self.hover_on = (self.hover_on + 1) % len(self.regions)
                case EventsEnum.ENTER:
                    self.activate_current_hover(globalstate)
                case EventsEnum.ESCAPE:
                    globalstate.to_remove = 1

    def reset(self) -> None:
        """
        Reset the highlighted region back to the first one.
        """
        self.hover_on = 0

    def region_status(self, index: int) -> str | None:
        """
        Return an optional status label for a region.

        Args:
            index: Index of the region in ``self.regions``.

        Returns:
            A short status string (e.g. ``"ON"``) or None when the region
            has no status. The base implementation always returns None.
        """
        return None
