from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @staticmethod
    def from_string(string: str) -> "Point":
        x, y = [int(p) for p in string.split(",")]
        return Point(x, y)

    def move(self, dx: int = 0, dy: int = 0) -> "Point":
        return Point(self.x + dx, self.y + dy)

    def distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class HorizontalOrVerticalLine:
    low: Point
    high: Point
    __horizontal: bool

    def __init__(self, end1: Point, end2: Point) -> None:
        if end1.x == end2.x:
            self.__horizontal = True

            if end1.y < end2.y:
                self.low = end1
                self.high = end2
            else:
                self.low = end2
                self.high = end1
        elif end1.y == end2.y:
            self.__horizontal = False
            if end1.x < end2.x:
                self.low = end1
                self.high = end2
            else:
                self.low = end2
                self.high = end1
        else:
            assert (
                False
            ), f"Given coordinates are neither horizontal, nor vertical: {self}"

    def online(self, p: Point) -> bool:
        if self.__horizontal:
            return p.x == self.low.x and self.low.y <= p.y <= self.high.y
        else:
            return p.y == self.low.y and self.low.x <= p.x <= self.high.x

    def points(self) -> Set[Point]:
        if self.__horizontal:
            return {Point(self.low.x, y) for y in range(self.low.y, self.high.y + 1)}
        else:
            return {Point(x, self.low.y) for x in range(self.low.x, self.high.x + 1)}


def draw_coordinates(
    points: Dict[Point, str], lines: List[HorizontalOrVerticalLine] = []
) -> str:
    min_x = min([p.x for p in points.keys()] + [l.low.x for l in lines])
    max_x = max([p.x for p in points.keys()] + [l.high.x for l in lines])
    min_y = min([p.y for p in points.keys()] + [l.low.y for l in lines])
    max_y = max([p.y for p in points.keys()] + [l.high.y for l in lines])

    out = ""

    for x in range(max_x, min_x - 1, -1):
        for y in range(min_y, max_y + 1):
            point = points.get(Point(x, y), None)
            out += (
                point
                if point is not None
                else ("#" if any(l.online(Point(x, y)) for l in lines) else ".")
            )
        out += "\n"

    return out
