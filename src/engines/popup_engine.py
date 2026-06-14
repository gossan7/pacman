from typing import Any

from .engine import Engine
from ..state import GlobalState


class PopupEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.popup = 0

    def update_focus(self, globalstate: GlobalState) -> None:
        self.popup = globalstate.popup

    def update_always(self, globalstate):
        pass
