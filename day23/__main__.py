from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, Generator, Iterator, List, Optional, Set, Tuple

from utils import file_lines
from utils.geometry import Point, draw_coordinates


class Direction(Enum):
    NW = "NW"
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"


def parse_field(fn: str) -> Generator[Tuple[int, int], None, None]:
    for x, l in enumerate(reversed(list(file_lines(fn)))):
        for y, c in enumerate(l):
            match c:
                case ".":
                    pass
                case "#":
                    yield (x, y)


def move_directions() -> Generator[List[Direction], None, None]:
    directions = [Direction.N, Direction.S, Direction.W, Direction.E]
    while True:
        yield directions
        directions.append(directions.pop(0))


def neighbors(elf: Tuple[int, int], direction: Direction) -> Set[Tuple[int, int]]:
    (x, y) = elf
    match direction:
        case Direction.E:
            return {(x + offset, y + 1) for offset in range(-1, 2)}
        case Direction.N:
            return {(x + 1, y + offset) for offset in range(-1, 2)}
        case Direction.W:
            return {(x + offset, y - 1) for offset in range(-1, 2)}
        case Direction.S:
            return {(x - 1, y + offset) for offset in range(-1, 2)}
        case _:
            assert False


def all_neighbors(elf: Tuple[int, int]) -> Set[Tuple[int, int]]:
    (x, y) = elf
    return {
        (n_x, n_y)
        for n_x in range(x - 1, x + 2)
        for n_y in range(y - 1, y + 2)
        if (n_x, n_y) != elf
    }


def move_elf(elf: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    (x, y) = elf
    match direction:
        case Direction.E:
            return (x, y + 1)
        case Direction.N:
            return (x + 1, y)
        case Direction.W:
            return (x, y - 1)
        case Direction.S:
            return (x - 1, y)
        case _:
            assert False


def proposals(
    field: Set[Tuple[int, int]], move_direction: Generator[List[Direction], None, None]
) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """
    Returns the proposed targets with a list of elves proposing
    """

    proposals: Dict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(lambda: [])

    directions = next(move_direction)
    for elf in field:
        if field.intersection(all_neighbors(elf)):
            for direction in directions:
                if not field.intersection(neighbors(elf, direction)):
                    proposals[move_elf(elf, direction)].append(elf)
                    break

    return proposals


def round(
    field: Set[Tuple[int, int]], move_direction: Generator[List[Direction], None, None]
) -> Set[Tuple[int, int]]:
    props = proposals(field, move_direction)
    props_no_dups = {k: v for k, v in props.items() if len(v) == 1}

    new_field = field.copy()

    for move_to, [elf] in props_no_dups.items():
        new_field.remove(elf)
        new_field.add(move_to)

    return new_field

def empty_fields(field: Set[Tuple[int, int]]) -> int:
    x_s = { x for (x, _) in field }
    min_x = min(x_s)
    max_x = max(x_s)
    y_s = { y for (_, y) in field }
    min_y = min(y_s)
    max_y = max(y_s)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(field)

def part1(fn: str) -> int:
    field: Set[Tuple[int, int]] = set(parse_field(fn))
    # print("== Initial State ==")
    # print(draw_coordinates({Point(x, y): "#" for (x, y) in field}))
    directions = move_directions()
    for r in range(10):
        field = round(field, directions)
        # print(f"\n== End of Round {r + 1} ==")
        # print(draw_coordinates({Point(x, y): "#" for (x, y) in field}))

    return empty_fields(field)


def part2(fn: str) -> float:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day23/sample')}")
print(f"Part1: {part1('day23/input')}")
# print(f"Part2 Sample: {part2('day23/sample')}")
# print(f"Part2: {part2('day23/input')}")
