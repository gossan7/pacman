from typing import Type, Any
from time import perf_counter, sleep

from ..engines import (
    Engine,
    MenuEngine,
    GameEngine,
    PauseEngine,
    CheatEngine,
    ScoreEngine
)
from ..renderers import (
    Renderer,
    MenuRenderer,
    GameRenderer,
    PauseRenderer,
    CheatRenderer,
    ScoreRenderer
)
from ..state import EngineFlag
from ..state import GlobalState
from .input_handler import InputHandler


ENGINES: list[tuple[EngineFlag, Type[Engine], Type[Renderer]]] = [
    (EngineFlag.MENU, MenuEngine, MenuRenderer),
    (EngineFlag.GAME, GameEngine, GameRenderer),
    (EngineFlag.PAUSE, PauseEngine, PauseRenderer),
    (EngineFlag.CHEAT, CheatEngine, CheatRenderer),
    (EngineFlag.SCORE, ScoreEngine, ScoreRenderer)
]


class Orchestrator:

    def __init__(self, config: dict[str, Any]) -> None:
        self.engines: dict[EngineFlag, tuple[Engine, Renderer]] = {}
        for engine_flag, engine_class, renderer_class in ENGINES:
            engine = engine_class(config)
            renderer = renderer_class(config, engine)
            self.engines[engine_flag] = (engine, renderer)

        self.config = config
        self.global_state = GlobalState()
        self.input_handler = InputHandler()
        self.frame_time = 1.0 / config["fps"]
        self.frame_start = perf_counter()

    def update_global_state(self) -> None:
        self.global_state.inputs = self.input_handler.get_formatted_inputs()

        now = perf_counter()
        self.global_state.delta_time = now - self.frame_start
        self.frame_start = now

    def wait_frame_time(self) -> None:
        elapsed = perf_counter() - self.frame_start
        sleep(max(0, self.frame_time - elapsed))

    def run(self) -> None:
        # TEMPORARY : artificial loop to break at some point
        i = 0  # TEMPORARY

        self.input_handler.start()
        while self.global_state.running:
            self.update_global_state()
            for flag in self.global_state.engine_stack:
                engine, renderer = self.engines[flag]
                # to add: catch the switch fullscreen/window (add in the
                # renderer or in another method)
                engine.update(self.global_state)
                renderer.render()
            self.wait_frame_time()
            i += 1  # TEMPORARY
            print(i)  # TEMPORARY
            if i >= 10:  # TEMPORARY
                self.global_state.running = False  # TEMPORARY

        self.input_handler.stop()

    def run_test(self, max_iterations: int = 10) -> None:
        """TO DELETE: to test the inputs if needed"""
        import time
        i = 0

        self.input_handler.start()

        while self.global_state.running and i < max_iterations:
            while not any(self.input_handler.formatted_inputs.values()):
                time.sleep(0.05)

            print(self.input_handler.get_formatted_inputs())
            i += 1

        self.input_handler.stop()
