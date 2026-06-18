from typing import Any

from .engine import Engine
from ..state import GlobalState


class PopupEngine(Engine):
    """
    Base engine for screens drawn as a popup over another screen.

    Tracks how many popups are currently stacked so the renderer can dim
    or offset the overlay appropriately.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the popup depth counter.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.popup = 0

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Cache the current popup depth from the shared state.

        Args:
            globalstate: The shared mutable game state.
        """
        self.popup = globalstate.popup

    def update_always(self, globalstate: GlobalState) -> None:
        """
        Run every frame; popups have no always-on logic by default.

        Args:
            globalstate: The shared mutable game state.
        """
        pass
