import cProfile
import enum
import math
import re
from typing import Dict, Generator, List, Optional, Set, Tuple

from utils import file_lines
from utils.geometry import Point
from utils.matrix import matrix_of_size


class JetPush(enum.Enum):
    left = "<"
    right = ">"


def jet(input_line: str) -> Generator[JetPush, None, None]:
    while True:
        for j in input_line:
            yield JetPush(j)


class MoveNotAllowedExeption(Exception):
    pass


class ComeToRestException(Exception):
    pass


class Rock:
    points: List[Point]

    def __init__(self, points: List[Point]) -> None:
        self.points = points

    def move_by_jet(self, jet_push: JetPush, chamber: "Chamber") -> "Rock":
        def move_point(p: Point, jet_push: JetPush) -> Point:
            match jet_push:
                case JetPush.left:
                    return p.move(-1)
                case JetPush.right:
                    return p.move(1)

        # Move horizontal by jet
        new_points = [move_point(p, jet_push) for p in self.points]
        new_rock = Rock(new_points)
        if any(p.x < 0 for p in new_points):
            return self

        if any(p.x > 6 for p in new_points):
            return self

        if chamber.collision(new_rock):
            return self

        return new_rock

    def move_down(self, chamber: "Chamber") -> "Rock":
        new_points = [p.move(dy=-1) for p in self.points]
        if any(p.y < 0 for p in new_points):
            raise ComeToRestException(self)
        new_rock = Rock(new_points)
        if chamber.collision(new_rock):
            raise ComeToRestException(self)
        else:
            return new_rock

    @staticmethod
    def horizontal_line(leftmost_point: Point) -> "Rock":
        return Rock([leftmost_point.move(dx) for dx in range(4)])

    @staticmethod
    def plus(middle_point: Point) -> "Rock":
        points = [middle_point.move(dx) for dx in range(-1, 2)]
        points.append(middle_point.move(dy=-1))
        points.append(middle_point.move(dy=1))
        return Rock(points)

    @staticmethod
    def L(bottom_right_corner: Point) -> "Rock":
        return Rock(
            [bottom_right_corner.move(dx) for dx in range(-2, 1)]
            + [bottom_right_corner.move(dy=dy) for dy in range(1, 3)]
        )

    @staticmethod
    def vertical_line(bottom_point: Point) -> "Rock":
        return Rock([bottom_point.move(dy=dy) for dy in range(4)])

    @staticmethod
    def square(bottom_right_corner: Point) -> "Rock":
        return Rock(
            [bottom_right_corner.move(dx, dy) for dy in range(2) for dx in range(-1, 1)]
        )


def drop_rock(rock: Rock, chamber: "Chamber") -> Generator[Rock, JetPush, Rock]:
    try:
        while True:
            jet_push = yield (rock)
            rock = rock.move_by_jet(jet_push, chamber)
            print("Moved by jet")
            print(chamber.draw(rock))
            rock = rock.move_down(chamber)
            print("Moved down")
            print(chamber.draw(rock))
    except ComeToRestException:
        print("Rock came to rest")
        chamber.rock_comes_to_rest(rock)
        print(chamber.draw(rock))
        return rock


def rocks_falling() -> Generator[Rock, int, None]:
    highest_rock = 0
    while True:
        highest_rock = yield Rock.horizontal_line(Point(2, highest_rock + 3))
        highest_rock = yield Rock.plus(Point(3, highest_rock + 4))
        highest_rock = yield Rock.L(Point(4, highest_rock + 3))
        highest_rock = yield Rock.vertical_line(Point(2, highest_rock + 3))
        highest_rock = yield Rock.square(Point(3, highest_rock + 3))


class Chamber:
    """
    7 columns, 0 is bottom
    """

    columns: List[List[bool]]
    heights: List[int]
    cut_lines: int

    def __init__(self) -> None:
        self.columns = [[False for _ in range(5)] for _ in range(7)]
        self.heights = [0 for _ in range(7)]
        self.cut_lines = 0

    def safe_get(self, x: int, y: int) -> bool:
        assert 0 <= x < 7
        assert 0 <= y

        try:
            return self.columns[x][y - self.cut_lines]
        except IndexError:
            self.columns = [
                c + [False for _ in range(y - len(c) + 5)] for c in self.columns
            ]
            self.reduce()
            return False

    def safe_set(self, x: int, y: int, value: bool) -> None:
        self.columns[x][y - self.cut_lines] = value

    def highest(self) -> int:
        return max(self.heights)

    def rock_comes_to_rest(self, rock: Rock) -> None:
        for p in rock.points:
            assert self.safe_get(p.x, p.y) == False
            self.safe_set(p.x, p.y, True)
            if self.heights[p.x] < p.y + 1:
                self.heights[p.x] = p.y + 1

    def draw(self, rock: Optional[Rock] = None) -> str:
        string = ""
        for y in range(len(self.columns[0]) - 1, -1, -1):
            string += "#"
            for x in range(7):
                if rock is not None and any(p.x == x and p.y - self.cut_lines == y for p in rock.points):
                    string += "@"
                else:
                    string += "$" if self.columns[x][y] else "."
            string += "#\n"
        string += "#" * 9
        return string

    def collision(self, rock: Rock) -> bool:
        return any(self.safe_get(p.x, p.y) for p in rock.points)

    def reduce(self) -> None:
        # Need to find a way across, in a way that I can move up, down, left, or up-left, down-left
        def find_path_across(start_y: int, start_x: int, cut_height: int, visited: Set[Tuple[int, int]] = set()) -> Optional[int]:
            if start_x >= 7:
                return cut_height
            elif not self.columns[start_x][start_y - self.cut_lines]:
            #elif not self.safe_get(start_x, start_y):
                return None
            else:
                for new_start_y in [
                    start_y - 1,
                    start_y,
                    start_y + 1
                ]:
                    for new_start_x in [
                        start_x,
                        start_x + 1
                    ]:
                        if new_start_x == start_x and new_start_y == start_y:
                            continue
                        if new_start_y < 0 or new_start_x < 0:
                            continue
                        if (new_start_x, new_start_y) in visited:
                            continue
                    new_cut_height = find_path_across(
                        new_start_y,
                        start_x + 1,
                        cut_height if new_start_y < cut_height else new_start_y,
                        visited | { (start_x, start_y) })

                    if new_cut_height is not None:
                        return new_cut_height

                return None

        for scan_height in range(self.highest(), 7, -1):
            cut_height = find_path_across(scan_height, 0, scan_height)
            if cut_height is not None:
                print(f"Cut at {cut_height}")
                self.columns = [ c[cut_height - self.cut_lines - 2:] for c in self.columns ]
                self.cut_lines += cut_height
                return


def part1(fn: str) -> int:
    jt = jet(next(file_lines(fn)))

    chamber = Chamber()

    rocks = rocks_falling()
    rock = next(rocks)

    for _ in range(2002):
        dropping_rock = drop_rock(rock, chamber)
        dr = next(dropping_rock)
        print("New Rock")
        print(chamber.draw(dr))
        try:
            while True:
                curr_jet = next(jt)
                dr = dropping_rock.send(curr_jet)
        except StopIteration:
            rock = rocks.send(chamber.highest() - chamber.cut_lines)
    return chamber.highest()


def part2(fn: str) -> int:
    raise NotImplementedError()


#print(f"Part1 Sample: {part1('day17/sample')}")
print(f"Part1: {part1('day17/input')}")
# (f"Part2 Sample: {part2('day17/sample')}")
# print(f"Part2: {part2('day17/input')}")
