from .engine import Engine
from ..state import GlobalState
from ..instances import Pacman, Map, Ghost
from ..state import EngineFlag
from ..pacman_types import Vec2


class GameEngine(Engine):
    def __init__(
            self,
            config: dict,
    ) -> None:
        super().__init__(config)
        self.flag = EngineFlag.GAME
        self.map: Map = Map(
            gum_val=config["gum_val"],
            supergum_val=config["supergum_val"],
            width=config["width"],
            height=config["height"],
            seed=config["seed"]
        )

        self.ghost_val: int = config["ghost_val"]
        self.level_max_time: int = config["level_max_time"]
        self.lives: int = config["lives"]

        self.pacman: Pacman = Pacman(Vec2(*self.map.middle))
        # => map.middle à ajouter

        self.ghost_1 = Ghost(Vec2(0, 0))
        self.ghost_2 = Ghost(Vec2(0, self.map.width - 1))
        self.ghost_3 = Ghost(Vec2(self.map.height - 1, 0))
        self.ghost_4 = Ghost(Vec2(self.map.height - 1, self.map.width - 1))

    def update_always(self, globalstate: GlobalState) -> None:
        # rien a priori
        pass

    def update_focus(self, globalstate: GlobalState) -> None:
        # avancer les entités vers leur directions
        # modifier la direction
        # check les colisions => peut etre dans le update always ?
        pass
