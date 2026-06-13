from mazegenerator import MazeGenerator
from .gum import Gum, SuperGum
from ..pacman_types import Vec2
from .direction import Direction

_DELTA: dict[Direction, Vec2] = {
    Direction.NORTH: Vec2(-1, 0),
    Direction.SOUTH: Vec2(1, 0),
    Direction.WEST: Vec2(0, -1),
    Direction.EAST: Vec2(0, 1),
}


class Cell:
    def __init__(
            self,
            walls: int,
            content: Gum | SuperGum | None
    ) -> None:
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
            seed: int = 0
    ) -> None:
        """Inits a maze then use it as a map
        Each cell has walls encoded on 4 bits so we can do
        bitwise operations with directions. Also inits supergums on the corners
        and gums everywhere"""

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
        self.gums_remaining: int = sum(
            1 for row in self.game_map
            for cell in row
            if cell.content is not None)

    def _make_content(self, walls: int, row: int,
                      col: int) -> Gum | SuperGum | None:
        if walls == 0b1111 or (row, col) == self.middle:
            return None
        if (row, col) in self._corners:
            return SuperGum(self._supergum_val)
        if (self.middle[0] - 2 < row < self.middle[0] + 2 or
                self.middle[1] - 3 < col < self.middle[1] + 3):
            return None
        return Gum(self._gum_val)

    def open_directions(self, position: Vec2) -> list[Direction]:
        return [d for d in (Direction.NORTH, Direction.SOUTH,
                            Direction.EAST, Direction.WEST)
                if self.can_move(position, d)]

    def can_move(self, position: Vec2, direction: Direction) -> bool:
        cell = self.game_map[position.row][position.col]
        return (cell.walls & direction) == 0

    def destination(self, position: Vec2, direction: Direction) -> Vec2:
        delta = _DELTA[direction]
        return Vec2(position.row + delta.row, position.col + delta.col)

    def delete_content(self, row: int, col: int) -> None:
        if self.game_map[row][col].content is not None:
            self.game_map[row][col].content = None
            self.gums_remaining -= 1
