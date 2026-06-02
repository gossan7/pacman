from .engine import Engine
from .global_state import GlobalState
from ..instances import Pacman, Map, Ghost
from .engine_flag import EngineFlag


class GameEngine(Engine):
    def __init__(
            self,
            config: dict,
            is_running: bool = True,
            is_listening: bool = True,
            seed: int = 0) -> None:
        super().__init__(is_running, is_listening)
        self.flag = EngineFlag.GAME
        self.map: Map = Map(
            gum_val=config['gum_val'],
            supergum_val=config['supergum_val'],
            width=config['width'],
            height=config['height'],
            seed=seed)
        self.ghost_val: int = config['ghost_val']
        self.level_max_time: int = config['level_max_time']
        self.lives: int = config['lives']
        self.pacman: list[Pacman, list[int, int]] = [
            Pacman(), self.map.middle]  # => map.middle à ajouter
        self.ghost_1: list[Ghost, list[int, int]] = [Ghost(), [0, 0]]
        self.ghost_2: list[Ghost, list[int, int]] = [
            Ghost(), [0, self.map.width - 1]]
        self.ghost_3: list[Ghost, list[int, int]] = [
            Ghost(), [self.map.height - 1, 0]]
        self.ghost_4: list[Ghost, tuple[int, int]] = [
            Ghost(), [self.map.height - 1, self.map.width - 1]]

    def update_always(self, globalstate: GlobalState) -> None:
        # rien a priori
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        # avancer les entités vers leur directions
        # modifier la direction
        # check les colisions => peut etre dans le update always ?
        pass
