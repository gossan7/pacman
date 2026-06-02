from .engine_flag import EngineFlag


class GlobalState:
    def __init__(self, delta_time: float) -> None:
        self.is_paused: bool = False
        self.focus: EngineFlag = EngineFlag.MENU
        self.cheat_enabled: bool = False
        self.delta_time: float = delta_time
        self.running: bool = True
        self.engine_stack: list[list[EngineFlag, bool]] = [
            [EngineFlag.MENU, True],
            [EngineFlag.GAME, False],
            [EngineFlag.PAUSE, False]
        ]
