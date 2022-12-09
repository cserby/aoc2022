from typing import Dict, Generator, Set, Tuple

from utils import draw_coordinates, file_lines


def move_tail(head_pos: Tuple[int, int], tail_pos: Tuple[int, int]) -> Tuple[int, int]:
    (head_x, head_y) = head_pos
    (tail_x, tail_y) = tail_pos

    d_x = head_x - tail_x
    d_y = head_y - tail_y

    if abs(d_x) < 2 and abs(d_y) < 2:
        return tail_pos

    mov_x = 0 if d_x == 0 else int(d_x / abs(d_x))
    mov_y = 0 if d_y == 0 else int(d_y / abs(d_y))

    return (tail_x + mov_x, tail_y + mov_y)


def move_head(head_pos: Tuple[int, int], dir: str) -> Tuple[int, int]:
    return {
        "U": (head_pos[0] + 1, head_pos[1]),
        "D": (head_pos[0] - 1, head_pos[1]),
        "R": (head_pos[0], head_pos[1] + 1),
        "L": (head_pos[0], head_pos[1] - 1),
    }[dir]


def rope_head_segment() -> Generator[
    Tuple[Tuple[int, int], Tuple[int, int]], str, None
]:
    head_pos = (0, 0)
    tail_pos = (0, 0)

    while True:
        dir = yield (head_pos, tail_pos)

        head_pos = move_head(head_pos, dir)
        tail_pos = move_tail(head_pos, tail_pos)


def part1(fn: str):
    gen = rope_head_segment()
    tail_pos = next(gen)[1]
    tail_poss = {tail_pos}
    for move in file_lines(fn):
        (dir, count) = move.split(" ")
        for _ in range(int(count)):
            tail_pos = gen.send(dir)[1]
            tail_poss.add(tail_pos)
    return len(tail_poss)


def rope_segment() -> Generator[
    Tuple[Tuple[int, int], Tuple[int, int]], Tuple[int, int], None
]:
    head_pos = (0, 0)
    tail_pos = (0, 0)

    while True:
        head_pos = yield (head_pos, tail_pos)
        tail_pos = move_tail(head_pos, tail_pos)


def part2(fn: str):
    head = rope_head_segment()
    next(head)
    segments = [rope_segment() for i in range(9)]
    [next(segment) for segment in segments]
    tail_poss: Set[Tuple[int, int]] = {(0, 0)}
    for move in file_lines(fn):
        (dir, count) = move.split(" ")
        for i in range(int(count)):
            coords: Dict[Tuple[int, int], str] = {(0, 0): "s"}
            head_head, head_tail = head.send(dir)
            next_segment_head = head_tail
            coords[head_head] = "H"
            for index, segment in enumerate(segments):
                segment_head, segment_tail = segment.send(next_segment_head)
                coords[segment_head] = f"{index + 1}"
                next_segment_head = segment_tail
                if index + 1 == 9:
                    tail_poss.add(segment_head)
    #            if i == int(count) - 1:
    #                print(draw_coordinates(coords))
    return len(tail_poss)


print(f"Part1 Sample: {part1('day9/sample')}")
print(f"Part1: {part1('day9/input')}")
print(f"Part2 Sample: {part2('day9/sample')}")
print(f"Part2 Sample2: {part2('day9/sample2')}")
print(f"Part2: {part2('day9/input')}")
