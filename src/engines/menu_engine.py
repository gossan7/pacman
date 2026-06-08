from typing import Any

from .engine import Engine
from ..state import GlobalState, EngineFlag, EventsEnum


REGIONS = [
    "PLAY",
    "SCORES",
    "CONTROLS",
    "OPTIONS",
    "QUIT"
]

ACTIONS = {
    "PLAY": (EngineFlag.GAME, 1),
    "SCORES": (EngineFlag.SCORES, 0),
    "COTROLS": (EngineFlag.CONTROLS, 0),
    "OPTIONS": (EngineFlag.OPTIONS, 0),
    "QUIT": (EngineFlag.QUIT, 0)
}


class MenuEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.MENU
        self.hover_on = 0

    def activate_current_hover(self, globalstate: GlobalState):
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.UP:
                    self.hover_on = (self.hover_on - 1) % len(REGIONS)
                case EventsEnum.DOWN:
                    self.hover_on = (self.hover_on + 1) % len(REGIONS)
                case EventsEnum.ENTER:
                    self.activate_current_hover(globalstate)
                case EventsEnum.ESCAPE:
                    globalstate.to_add = EngineFlag.QUIT
