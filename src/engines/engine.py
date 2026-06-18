from typing import Any
from abc import ABC, abstractmethod

from ..state import GlobalState
from ..state import EngineFlag


class Engine(ABC):
    """
    Abstract base class for all game engines (screens).

    Each engine owns the logic for one screen and is ticked every frame.
    ``update_always`` runs on every frame while the engine is on the stack;
    ``update_focus`` runs only when the engine is the focused one.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Store the config and initialise the engine flag.

        Args:
            config: Validated configuration dict shared by all engines.
        """
        self.flag = EngineFlag.NONE
        self.config = config

    @abstractmethod
    def update_always(self, globalstate: GlobalState) -> None:
        """
        Run logic that must execute on every frame.

        Args:
            globalstate: The shared mutable game state.
        """
        pass

    @abstractmethod
    def update_focus(self, globalstate: GlobalState) -> None:
        """
        Run logic that should execute only while this engine has focus.

        Args:
            globalstate: The shared mutable game state.
        """
        pass

    def update(self, globalstate: GlobalState) -> None:
        """
        Tick the engine, dispatching to the always/focus hooks.

        Args:
            globalstate: The shared mutable game state.
        """
        self.update_always(globalstate)
        if globalstate.focus == self.flag:
            self.update_focus(globalstate)

    def reset(self) -> None:
        """
        Reset the engine's state when it is popped from the stack.

        The base implementation does nothing; engines override it as needed.
        """
        pass
