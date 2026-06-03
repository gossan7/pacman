from .engine_flag import EngineFlag


class GlobalState:
    def __init__(self) -> None:
        self.focus: EngineFlag = EngineFlag.MENU
        self.cheat_enabled: bool = False
        self.delta_time: float = 0.0
        self.running: bool = True
        self.inputs: dict = {}
        self.engine_stack: list[EngineFlag] = [
            EngineFlag.MENU,
        ]
