from mazegenerator import MazeGenerator
from .gum import Gum, SuperGum


class Cell:
    def __init__(
            self,
            walls: int,
            content: Gum | SuperGum | None) -> None:
        self.walls: int = walls
        self.content = content


class Map:
    # Size of the 42 pattern in the middle
    _PATTERN_ROWS = 5
    _PATTERN_COLS = 7

    def __init__(
            self,
            gum_val: int = 10,
            supergum_val: int = 50,
            width: int = 20,
            height: int = 20,
            seed: int = 0) -> None:
        """Inits a maze then use it as a map
        Each cell has walls encoded on 4 bits so we can do
        bitwise operations with directions. Also inits supergums on the corners
        and gums everywhere

        TODO: delete the pacgum where pacman spawns"""

        self._mazegen: MazeGenerator = MazeGenerator(
            size=(width, height), perfect=False, seed=seed)

        self._corners = {(0, 0), (0, width - 1), (height - 1, 0),
                         (height - 1, width - 1)}

        self._gum_val: int = gum_val
        self._supergum_val: int = supergum_val
        self.height: int = height
        self.width: int = width
        self.middle: tuple[int, int] = (
            (self.height - self._PATTERN_ROWS) // 2 + self._PATTERN_ROWS // 2,
            (self.width - self._PATTERN_COLS) // 2 + self._PATTERN_COLS // 2,
        )

        self.game_map: list[list[Cell]] = [
            [
                Cell(
                    self._mazegen.maze[row][col],
                    self._make_content(
                        self._mazegen.maze[row][col],
                        row, col)
                )
                for col in range(width)
            ]
            for row in range(height)]

    def _make_content(self, walls: int, row: int,
                      col: int) -> Gum | SuperGum | None:
        if walls == 0b1111:
            return None
        if (row, col) in self._corners:
            return SuperGum(self._supergum_val)
        return Gum(self._gum_val)

    def delete_content(self, row: int, col: int) -> None:
        self.map[row][col].content = None
