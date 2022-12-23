from enum import Enum
from typing import Generator, List, Optional, Tuple

from utils import file_lines


class MazeCell(Enum):
    void = " "
    wall = "#"
    open = "."


class Direction(Enum):
    up = "^"
    down = "v"
    left = "<"
    right = ">"


class HitAWallException(Exception):
    pass


class WrapAroundHorizontallyToTheLeftException(Exception):
    pass


class WrapAroundHorizontallyToTheRightException(Exception):
    pass


class WrapAroundVerticallyToTheTopException(Exception):
    pass


class WrapAroundVerticallyToTheBottomException(Exception):
    pass


class Maze:
    _maze: List[List[MazeCell]]

    def __init__(self, lines: List[str]) -> None:
        self._maze = [[MazeCell(c) for c in l] for l in lines]

    def first_cell_from_left(self, row: int) -> Tuple[Tuple[int, int], MazeCell]:
        assert row > 0
        (col, c) = next(
            (col, c)
            for col, c in enumerate(self._maze[row - 1], 1)
            if c != MazeCell.void
        )

        return ((row, col), c)

    def first_cell_from_right(self, row: int) -> Tuple[Tuple[int, int], MazeCell]:
        assert row > 0
        (col, c) = list(
            (col, c)
            for col, c in enumerate(self._maze[row - 1], 1)
            if c != MazeCell.void
        )[-1]

        return ((row, col), c)

    def col(self, col: int) -> List[MazeCell]:
        assert col > 0
        c = []
        for l in self._maze:
            try:
                c.append(l[col - 1])
            except IndexError:
                c.append(MazeCell.void)
        return c

    def first_cell_from_top(self, col: int) -> Tuple[Tuple[int, int], MazeCell]:
        (row, c) = next(
            (i, c) for i, c in enumerate(self.col(col), 1) if c != MazeCell.void
        )

        return ((row, col), c)

    def first_cell_from_bottom(self, col: int) -> Tuple[Tuple[int, int], MazeCell]:
        (row, c) = list(
            (i, c) for i, c in enumerate(self.col(col), 1) if c != MazeCell.void
        )[-1]

        return ((row, col), c)

    def start_cell(self) -> Tuple[int, int]:
        (pos, cell) = self.first_cell_from_left(1)
        assert cell == MazeCell.open
        return pos

    def cell(self, pos: Tuple[int, int]) -> MazeCell:
        """
        Rows start from 1 at the top and count downward;
        columns start from 1 at the left and count rightward.
        """

        (row, col) = pos
        if row <= 0 or col <= 0:
            return MazeCell.void

        try:
            return self._maze[row - 1][col - 1]
        except IndexError:
            return MazeCell.void

    def move(self, position: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
        (row, col) = position
        match direction:
            case Direction.right:
                new_row = row
                new_col = col + 1
            case Direction.up:
                new_row = row - 1
                new_col = col
            case Direction.left:
                new_row = row
                new_col = col - 1
            case Direction.down:
                new_row = row + 1
                new_col = col

        c = self.cell((new_row, new_col))
        match c:
            case MazeCell.open:
                return (new_row, new_col)
            case MazeCell.wall:
                raise HitAWallException((new_row, new_col))
            case MazeCell.void:
                (pos, cell) = self.teleport((new_row, new_col), direction)
                match cell:
                    case MazeCell.wall:
                        raise HitAWallException(pos)
                    case MazeCell.open:
                        return pos
                    case _:
                        assert False

    def teleport(
        self, new_pos: Tuple[int, int], direction: Direction
    ) -> Tuple[Tuple[int, int], MazeCell]:
        (new_row, new_col) = new_pos
        match direction:
            case Direction.right:
                return self.first_cell_from_left(new_row)
            case Direction.up:
                return self.first_cell_from_bottom(new_col)
            case Direction.left:
                return self.first_cell_from_right(new_row)
            case Direction.down:
                return self.first_cell_from_top(new_col)
            case _:
                assert False

    def to_string(self, me: Optional["Me"]) -> str:
        string = ""
        for row, r in enumerate(self._maze, 1):
            for col, c in enumerate(r, 1):
                if me is not None and me.position == (row, col):
                    assert c == MazeCell.open
                    string += f"\033[93m{str(me)}\033[0m"
                    continue
                match c:
                    case MazeCell.void:
                        string += " "
                    case MazeCell.wall:
                        string += "#"
                    case MazeCell.open:
                        string += "."
            string += "\n"
        return string

    def __repr__(self) -> str:
        return self.to_string(None)


class Me:
    position: Tuple[int, int]
    direction: Direction

    def __init__(self, row: int, col: int) -> None:
        self.position = (row, col)
        self.direction = Direction.right

    def __repr__(self) -> str:
        return str(self.direction.value)

    def move_forward(self, steps: int, maze: Maze) -> None:
        try:
            for _ in range(steps):
                self.position = maze.move(self.position, self.direction)
        except HitAWallException:
            pass

    def turn(self, direction: str) -> None:
        assert direction in ["R", "L"]
        match direction:
            case "R":
                match self.direction:
                    case Direction.up:
                        self.direction = Direction.right
                    case Direction.right:
                        self.direction = Direction.down
                    case Direction.down:
                        self.direction = Direction.left
                    case Direction.left:
                        self.direction = Direction.up
            case "L":
                match self.direction:
                    case Direction.up:
                        self.direction = Direction.left
                    case Direction.left:
                        self.direction = Direction.down
                    case Direction.down:
                        self.direction = Direction.right
                    case Direction.right:
                        self.direction = Direction.up

    def password(self) -> int:
        """
        Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        The final password is the sum of 1000 times the row, 4 times the column, and the facing.
        """

        facing = -1
        match self.direction:
            case Direction.right:
                facing = 0
            case Direction.down:
                facing = 1
            case Direction.left:
                facing = 2
            case Direction.up:
                facing = 3
        assert facing != -1
        (row, col) = self.position
        return 1000 * row + 4 * col + facing


def instructions(line: str) -> Generator[int | str, None, None]:
    tmp: str = ""
    for c in line:
        try:
            int(c)
            tmp += c
        except ValueError:
            yield int(tmp)
            tmp = ""
            yield c
    assert tmp != ""
    yield int(tmp)


def part1(fn: str) -> int:
    input_lines = list(file_lines(fn))
    maze = Maze(input_lines[:-2])
    me = Me(*maze.start_cell())

    for instr in instructions(input_lines[-1]):
        print(f"Instruction: {instr}")
        match instr:
            case int():
                me.move_forward(instr, maze)
            case str():
                me.turn(instr)
        print(f"After instruction '{instr}':\n{maze.to_string(me)}")

    return me.password()


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day22/sample')}")
print(f"Part1: {part1('day22/input')}")
# print(f"Part2 Sample: {part2('day22/sample')}")
# print(f"Part2: {part2('day22/input')}")
