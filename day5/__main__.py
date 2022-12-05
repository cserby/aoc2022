from typing import Iterator, List

from utils import chunks, file_lines, take_while


def parse_initial_setup(file_lines: Iterator[str]) -> List[List[str]]:
    initial_setup = reversed(list(take_while(file_lines, lambda l: l != "")))
    number_of_columns = [int(chk[1]) for chk in chunks(next(initial_setup), 4, " ")][-1]
    columns: List[List[str]] = [[] for _ in range(number_of_columns)]
    for line in initial_setup:
        row = chunks(iter(line), 4, " ")
        for index, cell in enumerate(row):
            if cell[1] != " ":
                (columns[index]).append(cell[1])
    return columns


def instructions(instruction_lines: Iterator[str]):
    instructions = list(instruction_lines)
    for instruction in instructions:
        [move, count, frm, from_index, to, to_index] = instruction.split(" ")
        assert move == "move"
        assert frm == "from"
        assert to == "to"
        yield int(count), int(from_index), int(to_index)


def perform_instruction(
    columns: List[List[str]], count: int, from_index: int, to_index: int
) -> List[List[str]]:
    for _ in range(count):
        elem = columns[from_index - 1].pop()
        columns[to_index - 1].append(elem)
    return columns


def part1(file_name: str):
    fl = file_lines(file_name)
    columns = parse_initial_setup(fl)

    for (count, from_index, to_index) in instructions(fl):
        perform_instruction(columns, count, from_index, to_index)

    return "".join([c[-1] for c in columns])


def perform_instruction_2(
    columns: List[List[str]], count: int, from_index: int, to_index: int
) -> List[List[str]]:
    moved_elems = columns[from_index - 1][-count:]
    columns[from_index - 1] = columns[from_index - 1][:-count]
    columns[to_index - 1] += moved_elems
    return columns


def part2(file_name: str):
    fl = file_lines(file_name)
    columns = parse_initial_setup(fl)

    for (count, from_index, to_index) in instructions(fl):
        perform_instruction_2(columns, count, from_index, to_index)

    return "".join([c[-1] for c in columns])


print(f"Part1 Sample: {part1('day5/sample')}")
print(f"Part1: {part1('day5/input')}")
print(f"Part2 Sample: {part2('day5/sample')}")
print(f"Part2: {part2('day5/input')}")
