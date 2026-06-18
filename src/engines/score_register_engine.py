from typing import Any
import json

from .popup_engine import PopupEngine
from ..state import GlobalState
from ..state import EngineFlag, EventsEnum


MAX_NAME_LENGTH = 10


class ScoreRegisterEngine(PopupEngine):
    """
    End-of-game screen where the player types a name for the highscore.

    Collects typed characters (capped at ten), inserts the new entry into
    the table, persists it to the highscore file and returns to the menu.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise the name buffer and result fields.

        Args:
            config: Validated configuration dict.
        """
        super().__init__(config)
        self.flag = EngineFlag.SCORE_REGISTER
        self.name = ""
        self.score = 0
        self.won = False

    def update_always(self, globalstate: GlobalState) -> None:
        """
        Mirror the final score and win/lose result from shared state.

        Args:
            globalstate: The shared mutable game state.
        """
        super().update_always(globalstate)
        self.score = globalstate.score
        self.won = globalstate.won

    def _register(self, globalstate: GlobalState) -> None:
        """
        Insert the new entry into the table and save it to disk.

        Args:
            globalstate: The shared mutable game state.

        Raises:
            Exception: If writing the highscore file fails.
        """
        globalstate.scores.append((self.name.strip() or "???", self.score))
        globalstate.scores.sort(key=lambda x: x[1], reverse=True)
        while len(globalstate.scores) > 10:
            globalstate.scores.pop()
        self.name = ""

        json_object = [
            {"name": k, "score": v}
            for k, v in globalstate.scores
        ]

        try:
            with open(self.config["highscore_filename"], "+w") as f:
                json.dump(json_object, f)
        except Exception:
            raise Exception("Error during score writing into HIGHSCORE file.")

    def _close(self, globalstate: GlobalState) -> None:
        """
        Tear down the game stack and return to the main menu.

        Args:
            globalstate: The shared mutable game state.
        """
        globalstate.to_remove = len(globalstate.engine_stack)
        globalstate.to_add = EngineFlag.MENU

    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Edit the typed name and handle enter/backspace/escape.

        Args:
            globalstate: The shared mutable game state.
        """
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
