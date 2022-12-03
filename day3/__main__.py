from utils import file_lines


def split_in_half(line: str):
    length = len(line)
    return line[: int(length / 2)], line[int(length / 2) :]


def to_ord_set(comp: str):
    return {ord(ch) for ch in comp}


def find_common(compartment1: str, compartment2: str):
    comp1_ord_set = to_ord_set(compartment1)
    comp2_ord_set = to_ord_set(compartment2)
    return comp1_ord_set & comp2_ord_set


def ord_to_prio(ord: int):
    if 97 <= ord <= 122:
        return ord - 96
    else:
        return ord - 38


def part1(fn: str):
    return sum(
        [
            ord_to_prio(find_common(*split_in_half(line)).pop())
            for line in file_lines(fn)
        ]
    )


def part2(fn: str):
    pass


print(f"Part1 Sample: {part1('day3/sample')}")
print(f"Part1: {part1('day3/input')}")
# print(f"Part2 Sample: {part2('day3/sample')}")
# print(f"Part2: {part2('day3/input')}")
