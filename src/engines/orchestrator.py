from .engine import Engine
from .game_engine import GameEngine
from .menu_engine import MenuEngine
from .pause_engine import PauseEngine
from .engine_flag import EngineFlag
from ..renderers import MenuRenderer, GameRenderer, PauseRenderer, Renderer
from .global_state import GlobalState


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
        # self.inputs: list[inputtype] = [] => todo

    def run(self) -> None:
        # TEMPORARY : artificial loop to break at some point
        i = 0  # TEMPORARY
        while self.global_state.running:
            self.handle_inputs()
            for flag, present in self.global_state.engine_stack:
                if present:
                    engine, renderer = self.get_from_stack(flag)
                    engine.update(self.global_state)
                    renderer.render()
            i += 1  # TEMPORARY
            print(i)  # TEMPORARY
            if i >= 100:  # TEMPORARY
                self.global_state.running = False  # TEMPORARY

            self.clear_input()

    def get_from_stack(self, flag: EngineFlag) -> tuple[Engine, Renderer]:
        if flag == EngineFlag.MENU:
            return (self.menu_engine, self.menu_renderer)
        elif flag == EngineFlag.GAME:
            return (self.game_engine, self.game_renderer)
        elif flag == EngineFlag.PAUSE:
            return (self.pause_engine, self.pause_renderer)
        return (self.menu_engine, self.menu_renderer)

    def handle_inputs(self) -> None:
        # on garde la derniere direction input, on skip les autres
        # on garde une info d'input sur echap et on skip les autres
        # stocker dans self.inputs
        pass

    def clear_input(self) -> None:
        self.inputs = []
