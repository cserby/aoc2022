from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


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


@dataclass()
class HorizontalOrVerticalLine:
    end1: Point
    end2: Point
    horizontal: Optional[bool] = None

    def __post_init__(self) -> None:
        if self.end1.x == self.end2.x:
            self.horizontal = True
        elif self.end1.y == self.end2.y:
            self.horizontal = False
        else:
            assert (
                False
            ), f"Given coordinates are neither horizontal, nor vertical: {self}"

    def online(self, p: Point) -> bool:
        if self.horizontal:
            return p.x == self.end1.x and min(self.end1.y, self.end2.y) <= p.y <= max(
                self.end1.y, self.end2.y
            )
        else:
            return p.y == self.end1.y and min(self.end1.x, self.end2.x) <= p.x <= max(
                self.end1.x, self.end2.x
            )


def draw_coordinates(
    points: Dict[Point, str], lines: List[HorizontalOrVerticalLine] = []
) -> str:
    min_x = min(
        min(p.x for p in points.keys()),
        min(min(l.end1.x, l.end2.x) for l in lines),
    )
    max_x = max(
        max(p.x for p in points.keys()),
        max(max(l.end1.x, l.end2.x) for l in lines),
    )
    min_y = min(
        min(p.y for p in points.keys()),
        min(min(l.end1.y, l.end2.y) for l in lines),
    )
    max_y = max(
        max(p.y for p in points.keys()),
        max(max(l.end1.y, l.end2.y) for l in lines),
    )

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
