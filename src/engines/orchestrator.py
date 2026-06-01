from .engine import Engine
from .game_engine import GameEngine
from .menu_engine import MenuEngine
from .pause_engine import PauseEngine
from .engine_flag import EngineFlag
# add les renderers


class GlobalState:
    def __init__(self, delta_time: float) -> None:
        self.is_paused: bool = False
        self.focus: EngineFlag = EngineFlag.MENU
        self.cheat_enabled: bool = False
        self.delta_time: float = delta_time
        self.running: bool = True
        self.engine_stack: list[list[EngineFlag, bool]] = [
            [EngineFlag.MENU, True], [EngineFlag.GAME, False], [EngineFlag.PAUSE, False]]


class Orchestrator:

    def __init__(self, config: dict, delta_time: float) -> None:
        self.menu_engine = MenuEngine(True, True)
        self.menu_renderer = MenuRenderer(
            engine=self.menu_engine, config=config)

        self.game_engine = GameEngine(False, False)
        self.game_renderer = GameRenderer(
            engine=self.game_engine, config=config)

        self.pause_engine = PauseEngine(False, False)
        self.pause_renderer = PauseRenderer(
            engine=self.pause_engine, config=config)

        self.config: dict = config
        self.init_seed = config['seed']
        self.global_state: GlobalState = GlobalState(delta_time)
        # self.inputs: list[inputtype] = [] => todo

    def run(self) -> None:
        while self.global_state.running:
            self.handle_inputs()
            for flag, present in self.global_state.engine_stack:
                if present:
                    engine, renderer = self.get_from_stack(flag)
                    engine.update(self.global_state)
                    renderer.render(self.global_state)
            # self.update_engine_stack() => plus besoin on le fais dans
            # l'update de l'engine
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

    def clear_input(self) -> None:
        self.inputs = []
