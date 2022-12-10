from typing import Iterator

from utils import file_lines


def cathode_ray(instructions: Iterator[str]):
    x = 1
    for instruction in instructions:
        if instruction.startswith("addx"):
            add = int(instruction.split(" ")[1])
            for _ in range(2):
                yield x
            x += add
        elif instruction == "noop":
            yield x
        else:
            assert False, instruction
    yield x


def part1(fn: str):
    interesting = [20, 60, 100, 140, 180, 220]
    cat_ray = cathode_ray(file_lines(fn))
    states = list(cat_ray)
    return sum(i * states[i - 1] for i in interesting)


def part2(fn: str):
    pass


# print(f"Part1 Sample: {part1('day10/sample')}")
print(f"Part1 Sample2: {part1('day10/sample2')}")
print(f"Part1: {part1('day10/input')}")
# print(f"Part2 Sample: {part2('day10/sample')}")
# print(f"Part2 Sample2: {part2('day10/sample2')}")
# print(f"Part2: {part2('day10/input')}")
