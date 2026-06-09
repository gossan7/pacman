from typing import Any
from abc import abstractmethod

from .engine import Engine
from ..state import GlobalState, EventsEnum


class RegionPopupEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.regions = ["NONE"]
        self.hover_on = 0
        self.text_to_display: str = ""

    @abstractmethod
    def activate_current_hover(self, globalstate: GlobalState) -> None:
        pass

    def update_always(self, globalstate: GlobalState) -> None:
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

    def update_focus(self, globalstate: GlobalState) -> None:
        pass
