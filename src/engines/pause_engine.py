from collections import deque

from .region_popup_engine import RegionPopupEngine
from ..state import EngineFlag, GlobalState, EventsEnum


REGIONS = [
    "RESUME",
    "CONTROLS",
    "QUIT"
]

ACTIONS = {
    "RESUME": (None, 1),
    "CONTROLS": (EngineFlag.CONTROLS, 0),
    "QUIT": (EngineFlag.QUIT, 0)
}

TEXT_TO_DISPLAY = "PAUSE"


KONAMI_CODE = [
    EventsEnum.UP,
    EventsEnum.DOWN,
    EventsEnum.LEFT,
    EventsEnum.RIGHT,
    EventsEnum.LEFT,
    EventsEnum.RIGHT
]


class PauseEngine(RegionPopupEngine):
    def __init__(self, config):
        super().__init__(config)
        self.flag = EngineFlag.PAUSE
        self.regions = REGIONS
        self.text_to_display = TEXT_TO_DISPLAY
        self.current_input_seq = deque()

    def activate_current_hover(self, globalstate: GlobalState) -> None:
        to_add, to_remove = ACTIONS[REGIONS[self.hover_on]]
        if REGIONS[self.hover_on] == "QUIT":
            globalstate.to_add_on_quit = EngineFlag.MENU
        globalstate.to_remove += to_remove
        if to_add:
            globalstate.to_add = to_add

    def handle_konami(self, event: EventsEnum):
        self.current_input_seq.append(event)
        while len(self.current_input_seq) > len(KONAMI_CODE):
            self.current_input_seq.popleft()
        if list(self.current_input_seq) == KONAMI_CODE:
            return True
        return False

    def update_focus(self, globalstate: GlobalState) -> None:
        self.popup = globalstate.popup
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.UP:
                    self.hover_on = (self.hover_on - 1) % len(self.regions)
                case EventsEnum.DOWN:
                    self.hover_on = (self.hover_on + 1) % len(self.regions)
                case EventsEnum.ENTER:
                    self.current_input_seq = deque()
                    self.activate_current_hover(globalstate)
                case EventsEnum.ESCAPE:
                    self.current_input_seq = deque()
                    globalstate.to_remove = 1
            if event in {
                EventsEnum.UP,
                EventsEnum.DOWN,
                EventsEnum.LEFT,
                EventsEnum.RIGHT
            }:
                if self.handle_konami(event):
                    globalstate.to_add = EngineFlag.CHEAT
