from .engine_flag import EngineFlag
from .events_enum import EventsEnum


class GlobalState:
    def __init__(self) -> None:
        self.focus: EngineFlag = EngineFlag.MENU
        self.cheat_enabled: bool = False
        self.delta_time: float = 0.0
        self.running: bool = True
        self.events: list[EventsEnum] = []
        self.to_add: EngineFlag | None = None
        self.to_remove: int = 0
        self.engine_stack: list[EngineFlag] = [
            EngineFlag.MENU,
        ]
        self.score: int = 0
        self.won: bool = False
        self.to_quit: int = 1
        self.to_add_on_quit: EngineFlag | None = None
        self.popup: int = 0
