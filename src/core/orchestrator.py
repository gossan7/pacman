from typing import Type, Any
from time import perf_counter, sleep
import pyray

from ..engines import (
    Engine,
    MenuEngine,
    GameEngine,
    PauseEngine,
    CheatEngine,
    ScoresEngine,
    QuitEngine,
    ControlsEngine,
    ScoreRegisterEngine
)
from ..renderers import (
    Renderer,
    WindowHandler,
    MenuRenderer,
    GameRenderer,
    RegionPopupRenderer,
    ScoresRenderer,
    ControlsRenderer,
    ScoreRegisterRenderer
)
from ..state import EngineFlag, GlobalState
from .input_handler import InputHandler


ENGINES: list[tuple[EngineFlag, Type[Engine], Type[Renderer]]] = [
    (EngineFlag.MENU, MenuEngine, MenuRenderer),
    (EngineFlag.GAME, GameEngine, GameRenderer),
    (EngineFlag.PAUSE, PauseEngine, RegionPopupRenderer),
    (EngineFlag.CHEAT, CheatEngine, RegionPopupRenderer),
    (EngineFlag.SCORES, ScoresEngine, ScoresRenderer),
    (EngineFlag.QUIT, QuitEngine, RegionPopupRenderer),
    (EngineFlag.CONTROLS, ControlsEngine, ControlsRenderer),
    (EngineFlag.SCORE_REGISTER, ScoreRegisterEngine, ScoreRegisterRenderer)
]


class Orchestrator:
    """
    Owns the main game loop and the stack of engines/renderers.

    Builds every engine and its renderer, drives input collection, ticks
    the active engines each frame, draws them and enforces the target frame
    rate. The engine stack determines which screens are visible and which
    one currently has focus.
    """

    def __init__(
        self,
        config: dict[str, Any],
        scores: list[tuple[str, int]] | None = None
    ) -> None:
        """
        Build the engines, renderers and shared state.

        Args:
            config: Validated configuration dict.
            scores: Existing highscore entries, or None for an empty table.
        """
        self.window_handler = WindowHandler()
        self.engines: dict[EngineFlag, tuple[Engine, Renderer]] = {}
        for engine_flag, engine_class, renderer_class in ENGINES:
            engine = engine_class(config)
            renderer = renderer_class(config, engine, self.window_handler)
            self.engines[engine_flag] = (engine, renderer)

        self.config = config
        self.global_state = GlobalState(scores)
        self.input_handler = InputHandler()
        self.frame_time = 1.0 / config["fps"]
        self.frame_start = perf_counter()

    def update_global_state(self) -> None:
        """
        Advance the shared state at the end of a frame.

        Refreshes input events, applies pending pushes/pops on the engine
        stack (keeping the popup counter in sync), updates the focused
        engine, computes the frame delta time and decides whether the loop
        should keep running.
        """
        self.global_state.events = self.input_handler.get_formatted_inputs()
        self.global_state.chars = self.input_handler.chars

        for _ in range(min(self.global_state.to_remove,
                           len(self.global_state.engine_stack))):
            engine = self.global_state.engine_stack.pop()
            self.engines[engine][0].reset()
            if engine in {
                EngineFlag.PAUSE,
                EngineFlag.CHEAT,
                EngineFlag.SCORES,
                EngineFlag.QUIT,
                EngineFlag.CONTROLS
            }:
                self.global_state.popup -= 1

        self.global_state.to_remove = 0
        if self.global_state.to_add is not None:
            self.global_state.engine_stack.append(self.global_state.to_add)
        if self.global_state.to_add in {
            EngineFlag.PAUSE,
            EngineFlag.CHEAT,
            EngineFlag.SCORES,
            EngineFlag.QUIT,
            EngineFlag.CONTROLS
        }:
            self.global_state.popup += 1
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
        """
        Sleep until the target frame duration has elapsed.
        """
        elapsed = perf_counter() - self.frame_start
        sleep(max(0, self.frame_time - elapsed))

    def loop_start(self) -> None:
        """
        Begin a frame: open drawing and clear the background.
        """
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)

    def loop_end(self) -> None:
        """
        End a frame by flushing the draw calls to the window.
        """
        pyray.end_drawing()

    def run(self) -> None:
        """
        Run the main loop until no engine remains or the window closes.

        Starts the input listener, then each frame updates the window,
        ticks and renders every engine on the stack, throttles to the
        frame rate and refreshes the shared state. Stops the listener on
        exit.
        """
        self.input_handler.start()
        while self.global_state.running:
            self.window_handler.update(self.global_state)
            self.loop_start()
            for flag in self.global_state.engine_stack:
                engine, renderer = self.engines[flag]

                engine.update(self.global_state)
                renderer.render()
            self.loop_end()
            self.wait_frame_time()
            self.update_global_state()

        self.input_handler.stop()
