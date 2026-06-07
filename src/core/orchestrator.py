from typing import Type, Any
from time import perf_counter, sleep
import pyray

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
    WindowHandler,
    MenuRenderer,
    GameRenderer,
    PauseRenderer,
    CheatRenderer,
    ScoreRenderer
)
from ..state import EngineFlag, GlobalState
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
        self.window_handler = WindowHandler()
        self.engines: dict[EngineFlag, tuple[Engine, Renderer]] = {}
        for engine_flag, engine_class, renderer_class in ENGINES:
            engine = engine_class(config)
            renderer = renderer_class(config, engine, self.window_handler)
            self.engines[engine_flag] = (engine, renderer)

        self.config = config
        self.global_state = GlobalState()
        self.input_handler = InputHandler()
        self.frame_time = 1.0 / config["fps"]
        self.frame_start = perf_counter()

    def update_global_state(self) -> None:
        self.global_state.events = self.input_handler.get_formatted_inputs()

        for _ in range(min(self.global_state.to_remove,
                           len(self.global_state.engine_stack))):
            self.global_state.engine_stack.pop()
        self.global_state.to_remove = 0

        if self.global_state.to_add is not None:
            self.global_state.engine_stack.append(self.global_state.to_add)
        self.global_state.to_add = None

        if self.global_state.engine_stack:
            self.global_state.focus = self.global_state.engine_stack[-1]

        if len(self.global_state.engine_stack) == 0:
            self.global_state.running = False

        if pyray.window_should_close():
            self.global_state.running = False

        now = perf_counter()
        self.global_state.delta_time = now - self.frame_start
        self.frame_start = now

    def wait_frame_time(self) -> None:
        elapsed = perf_counter() - self.frame_start
        sleep(max(0, self.frame_time - elapsed))

    def loop_start(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)

    def loop_end(self):
        pyray.end_drawing()

    def run(self) -> None:
        # TEMPORARY : artificial loop to break at some point
        # i = 0  # TEMPORARY

        self.input_handler.start()
        while self.global_state.running:
            self.window_handler.update(self.global_state)
            self.loop_start()
            for flag in self.global_state.engine_stack:
                engine, renderer = self.engines[flag]
                # to add: catch the switch fullscreen/window (add in the
                # renderer or in another method)
                engine.update(self.global_state)
                renderer.render()
            self.loop_end()
            self.wait_frame_time()
            self.update_global_state()
            # i += 1  # TEMPORARY
            # print(i)  # TEMPORARY
            # if i >= 10:  # TEMPORARY
            # self.global_state.running = False  # TEMPORARY

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
