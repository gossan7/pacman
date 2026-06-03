from ..engines import Engine
from ..engines import GameEngine
from ..engines import MenuEngine
from ..engines import PauseEngine
from ..state import EngineFlag
from ..renderers import MenuRenderer, GameRenderer, PauseRenderer, Renderer
from ..state import GlobalState
from .input_controller import InputController


class Orchestrator:

    def __init__(self, config: dict, delta_time: float) -> None:
        self.menu_engine = MenuEngine()
        self.menu_renderer = MenuRenderer(
            engine=self.menu_engine, config=config)

        self.game_engine = GameEngine(config=config, seed=config['seed'])
        self.game_renderer = GameRenderer(
            engine=self.game_engine, config=config)

        self.pause_engine = PauseEngine()
        self.pause_renderer = PauseRenderer(
            engine=self.pause_engine, config=config)

        self.config: dict = config
        self.init_seed = config['seed']
        self.global_state: GlobalState = GlobalState(delta_time)

        self.input_controller: InputController = InputController()

    def run(self) -> None:
        # TEMPORARY : artificial loop to break at some point
        i = 0  # TEMPORARY

        self.input_controller.start()

        while self.global_state.running:
            controls = dict(self.input_controller.formatted_inputs)
            for flag, present in self.global_state.engine_stack:
                if present:
                    engine, renderer = self.get_from_stack(flag)
                    engine.update(self.global_state, controls)
                    print(controls)
                    renderer.render() # to add: catch the switch fullscreen/window (add in the render or in another method)
            i += 1  # TEMPORARY
            print(i)  # TEMPORARY
            if i >= 10:  # TEMPORARY
                self.global_state.running = False  # TEMPORARY

            self.input_controller.clear_input()

        self.input_controller.stop()

    def get_from_stack(self, flag: EngineFlag) -> tuple[Engine, Renderer]:
        if flag == EngineFlag.MENU:
            return (self.menu_engine, self.menu_renderer)
        elif flag == EngineFlag.GAME:
            return (self.game_engine, self.game_renderer)
        elif flag == EngineFlag.PAUSE:
            return (self.pause_engine, self.pause_renderer)
        return (self.menu_engine, self.menu_renderer)
