from typing import Generator, Tuple

from utils import file_lines


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


def rope_head_tail() -> Generator[Tuple[int, int], str, None]:
    head_pos = (0, 0)
    tail_pos = (0, 0)

    while True:
        dir = yield tail_pos

        head_pos = move_head(head_pos, dir)
        tail_pos = move_tail(head_pos, tail_pos)


def part1(fn: str):
    gen = rope_head_tail()
    tail_pos = next(gen)
    tail_poss = { tail_pos }
    for move in file_lines(fn):
        (dir, count) = move.split(" ")
        for _ in range(int(count)):
            tail_pos = gen.send(dir)
            tail_poss.add(tail_pos)
    return len(tail_poss)



def part2(fn: str):
    file_lines(fn)


print(f"Part1 Sample: {part1('day9/sample')}")
print(f"Part1: {part1('day9/input')}")
#print(f"Part2 Sample: {part2('day9/sample')}")
#print(f"Part2: {part2('day9/input')}")
