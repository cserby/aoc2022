import enum
import os
from typing import Callable, Generator, List, Optional, Set, Tuple

from utils import file_lines
from utils.geometry import Point
import cProfile


class JetPush(enum.Enum):
    left = "<"
    right = ">"


def jet(input_line: str) -> Generator[JetPush, None, None]:
    while True:
        for j in input_line:
            yield JetPush(j)


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
    def horizontal_line(highest: int) -> "Rock":
        return Rock([Point(2, highest + 3).move(dx) for dx in range(4)])

    @staticmethod
    def plus(highest: int) -> "Rock":
        middle_point = Point(3, highest + 4)
        points = [middle_point.move(dx) for dx in range(-1, 2)]
        points.append(middle_point.move(dy=-1))
        points.append(middle_point.move(dy=1))
        return Rock(points)

    @staticmethod
    def L(highest: int) -> "Rock":
        bottom_right_corner = Point(4, highest + 3)
        return Rock(
            [bottom_right_corner.move(dx) for dx in range(-2, 1)]
            + [bottom_right_corner.move(dy=dy) for dy in range(1, 3)]
        )

    @staticmethod
    def vertical_line(highest: int) -> "Rock":
        bottom_point = Point(2, highest + 3)
        return Rock([bottom_point.move(dy=dy) for dy in range(4)])

    @staticmethod
    def square(highest: int) -> "Rock":
        bottom_right_corner = Point(3, highest + 3)
        return Rock(
            [bottom_right_corner.move(dx, dy) for dy in range(2) for dx in range(-1, 1)]
        )


class Chamber:
    """
    7 columns, 0 is bottom
    """

    columns: List[List[bool]]
    offset: int
    jet_gen: Generator[JetPush, None, None]
    rock_gen: Generator[Callable[[int], Rock], None, None]

    def __init__(self, jet_gen: Generator[JetPush, None, None]) -> None:
        def rock_gen() -> Generator[Callable[[int], Rock], None, None]:
            while True:
                yield Rock.horizontal_line
                yield Rock.plus
                yield Rock.L
                yield Rock.vertical_line
                yield Rock.square

        self.columns = [[False for _ in range(5)] for _ in range(7)]
        self.offset = 0
        self.jet_gen = jet_gen
        self.rock_gen = rock_gen()

    def safe_get(self, x: int, y: int) -> bool:
        assert 0 <= x < 7
        assert 0 <= y

        normalized_y = y - self.offset

        assert normalized_y >= 0

        if normalized_y >= len(self.columns[x]):
            self.columns = [
                c + [False for _ in range(normalized_y - len(c) + 1)]
                for c in self.columns
            ]

        return self.columns[x][normalized_y]

    def safe_set(self, x: int, y: int, value: bool) -> None:
        self.columns[x][y - self.offset] = value

    def highest(self) -> int:
        highests = []
        for col in self.columns:
            try:
                highests.append(len(col) - list(reversed(col)).index(True))
            except ValueError:
                highests.append(0)
        return max(highests) + self.offset

    def rock_comes_to_rest(self, rock: Rock) -> None:
        for p in rock.points:
            assert self.safe_get(p.x, p.y) == False
            self.safe_set(p.x, p.y, True)
        if len(self.columns[0]) > 40:
            self.reduce()

    def draw(self, rock: Optional[Rock] = None) -> str:
        string = ""
        for y in range(len(self.columns[0]) - 1, -1, -1):
            string += f"{y:0>2} #"
            for x in range(7):
                if rock is not None and any(
                    p.x == x and p.y - self.offset == y for p in rock.points
                ):
                    string += "@"
                else:
                    string += "$" if self.columns[x][y] else "."
            string += "#\n"
        string += "#" * 12
        return string

    def collision(self, rock: Rock) -> bool:
        return any(self.safe_get(p.x, p.y) for p in rock.points)

    def reduce(self) -> None:
        fillable = [[1 if c else 0 for c in l] for l in self.columns]

        def draw_fillable() -> str:
            string = ""
            for y in range(len(fillable[0]) - 1, -1, -1):
                string += f"{y:0>2} #"
                for x in range(7):
                    string += str(fillable[x][y])
                string += "#\n"
            string += "#" * 12
            return string

        def fill(fillable: List[List[int]], pos: Tuple[int, int]) -> List[List[int]]:
            (x, y) = pos
            if fillable[x][y] == 1:
                return fillable

            for (n_x, n_y) in [
                (n_x, n_y)
                for n_x in range(max(x - 1, 0), x + 2)
                for n_y in range(max(y - 1, 0), y + 2)
            ]:
                try:
                    if fillable[n_x][n_y] == 0:
                        fillable[n_x][n_y] = 2
                        fill(fillable, (n_x, n_y))
                except IndexError:
                    pass

            return fillable

        for x in range(7):
            fill(fillable, (x, len(fillable[x]) - 1))
            #print(draw_fillable())

        lowest_twos = []
        for l in fillable:
            try:
                lowest_twos.append(l.index(2))
            except ValueError:
                lowest_twos.append(0)
        cut = min(lowest_twos) - 1
        #os.system("clear")
        #print(f"Cut at {cut}")
        #print(self.draw(None))
        #input()
        if cut > 0:
            self.columns = [ c[cut:] for c in self.columns ]
            self.offset += cut
        #print(f"Cut done at {cut}")
        #print(self.draw(None))

    def drop_rock(self, rock: Rock) -> None:
        try:
            while True:
                jet_push = next(self.jet_gen)
                rock = rock.move_by_jet(jet_push, self)
                #os.system("clear")
                #print("Moved by jet")
                #print(self.draw(rock))
                #input()
                rock = rock.move_down(self)
                #os.system("clear")
                #print("Moved down")
                #print(self.draw(rock))
                #input()
        except ComeToRestException:
            #os.system("clear")
            #print("Rock came to rest")
            self.rock_comes_to_rest(rock)
            #print(self.draw(rock))
            #input()


def part1(fn: str) -> int:
    chamber = Chamber(jet(next(file_lines(fn))))

    for _ in range(2022):
        rock = next(chamber.rock_gen)(chamber.highest())
        #os.system("clear")
        #print(f"New rock: {rock}")
        #print(chamber.draw(rock))
        chamber.drop_rock(rock)
    return chamber.highest()


def part2(fn: str) -> int:
    chamber = Chamber(jet(next(file_lines(fn))))

    for _ in range(1000000000000):
        rock = next(chamber.rock_gen)(chamber.highest())
        #os.system("clear")
        #print(f"New rock: {rock}")
        #print(chamber.draw(rock))
        chamber.drop_rock(rock)
    return chamber.highest()


print(f"Part1 Sample: {part1('day17/sample')}")
print(f"Part1: {part1('day17/input')}")
print(f"Part2 Sample: {part2('day17/sample')}")
print(f"Part2: {part2('day17/input')}")")
