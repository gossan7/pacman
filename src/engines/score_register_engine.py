from typing import Any

from .popup_engine import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


MAX_NAME_LENGTH = 12


class ScoreRegisterEngine(PopupEngine):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.flag = EngineFlag.SCORE_REGISTER
        self.name = ""
        self.score = 0
        self.won = False

    def update_always(self, globalstate: GlobalState) -> None:
        super().update_always(globalstate)
        self.score = globalstate.score
        self.won = globalstate.won

    def _register(self, globalstate: GlobalState) -> None:
        globalstate.scores.append((self.name.strip() or "???", self.score))
        globalstate.scores.sort(reverse=True)
        while len(globalstate.scores) > 10:
            globalstate.scores.pop()
        self.name = ""

    def _close(self, globalstate: GlobalState) -> None:
        globalstate.to_remove = len(globalstate.engine_stack)
        globalstate.to_add = EngineFlag.MENU

    def update_focus(self, globalstate: GlobalState) -> None:
        for char in globalstate.chars:
            if len(self.name) < MAX_NAME_LENGTH:
                self.name += char
        while globalstate.events:
            event = globalstate.events.pop()
            match event:
                case EventsEnum.ENTER:
                    self._register(globalstate)
                    self._close(globalstate)
                case EventsEnum.BACKSPACE:
                    self.name = self.name[:-1]
                case EventsEnum.ESCAPE:
                    self._close(globalstate)
