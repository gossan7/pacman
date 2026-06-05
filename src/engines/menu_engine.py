from typing import Any
from enum import Enum

from .engine import Engine
from ..state import GlobalState, EngineFlag, EventsEnum


class MenuRegionEnum(Enum):
    PLAY = 0
    SCORES = 1
    CONTROLS = 2
    OPTIONS = 3
    QUIT = 4


REGIONS = [
    MenuRegionEnum.PLAY,
    MenuRegionEnum.SCORES,
    MenuRegionEnum.CONTROLS,
    MenuRegionEnum.OPTIONS,
    MenuRegionEnum.QUIT
]

REGIONS_STR = {
    MenuRegionEnum.PLAY: "PLAY",
    MenuRegionEnum.SCORES: "SCORES",
    MenuRegionEnum.CONTROLS: "CONTROLS",
    MenuRegionEnum.OPTIONS: "OPTIONS",
    MenuRegionEnum.QUIT: "QUIT"
}

ACTIONS = {
    MenuRegionEnum.PLAY: (EngineFlag.GAME, True),
    MenuRegionEnum.SCORES: (EngineFlag.SCORES, False),
    MenuRegionEnum.CONTROLS: (EngineFlag.CONTROLS, False),
    MenuRegionEnum.OPTIONS: (EngineFlag.OPTIONS, False),
    MenuRegionEnum.QUIT: (EngineFlag.QUIT, False)
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
                    self.hover_on = (self.hover_on - 1) % len(REGIONS)
                case EventsEnum.DOWN:
                    self.hover_on = (self.hover_on + 1) % len(REGIONS)
                case EventsEnum.ENTER:
                    self.activate_current_hover(globalstate)
                case EventsEnum.ESCAPE:
                    globalstate.to_add = EngineFlag.QUIT
