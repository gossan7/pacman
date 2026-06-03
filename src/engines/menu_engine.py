from typing import Any
from enum import Enum

from .engine import Engine
from ..state import GlobalState, EngineFlag, EventsEnum


class RegionEnum(Enum):
    START = 0,
    SCORE = 1
    OPTIONS = 2,
    QUIT = 3


REGIONS = [
    RegionEnum.START,
    RegionEnum.SCORE,
    RegionEnum.OPTIONS,
    RegionEnum.QUIT
]

ACTIONS = {
    RegionEnum.START: (EngineFlag.GAME, True),
    RegionEnum.SCORE: (EngineFlag.SCORE, False),
    RegionEnum.OPTIONS: (EngineFlag.OPTIONS, False),
    RegionEnum.QUIT: (EngineFlag.QUIT, False)
}


class MenuEngine(Engine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.MENU
        self.hover_on = 0

    def activate_current_hover(self, globalstate: GlobalState):
        to_add, remove = ACTIONS[REGIONS[self.hover_on]]
        globalstate.to_remove += 1 if remove else 0
        globalstate.to_add = to_add

    def update_always(self, globalstate: GlobalState) -> None:
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.UP:
                    self.hover_on = max(self.hover_on - 1, 0)
                    print("feur 1")
                case EventsEnum.DOWN:
                    self.hover_on = min(self.hover_on + 1, len(REGIONS) - 1)
                    print("feur 2")
                case EventsEnum.ENTER:
                    self.activate_current_hover(globalstate)
                    print("feur 3")
                case EventsEnum.ESCAPE:
                    globalstate.to_add = EngineFlag.QUIT
                    print("feur 4")
