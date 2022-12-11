import math
from dataclasses import dataclass
from typing import Callable, List

from utils import file_lines, match_into_chunks


def drop_prefix(line: str, prefix: str):
    assert line.startswith(prefix)
    return line[len(prefix) :]


def parse_monkey_index(line: str) -> int:
    line = drop_prefix(line, "Monkey ")
    assert line.endswith(":")
    return int(line[: -len(":")])


def parse_items(line: str) -> List[int]:
    return [int(i.strip()) for i in drop_prefix(line, "  Starting items: ").split(",")]


def parse_operation(line: str) -> Callable[[int], int]:
    return eval(drop_prefix(line, "  Operation: ").replace("new =", "lambda old:"))


def parse_divisor(line: str) -> int:
    return int(drop_prefix(line, "  Test: divisible by "))


def parse_true_dest(line: str) -> int:
    return int(drop_prefix(line, "    If true: throw to monkey "))


def Parse_false_dest(line: str) -> int:
    return int(drop_prefix(line, "    If false: throw to monkey "))


@dataclass()
class Monkey:
    items: List[int]
    operation: Callable[[int], int]
    divisor: int
    true_dest: int
    false_dest: int
    inspected: int = 0

    def round(self, monkeys: List["Monkey"]) -> List["Monkey"]:
        for item in self.items:
            new_worry = int(math.floor(self.operation(item) / 3))
            monkeys[
                (self.true_dest if (new_worry % self.divisor == 0) else self.false_dest)
            ].items.append(new_worry)
            self.inspected += 1
        self.items = []
        return monkeys


def parse_monkey(lines: List[str]) -> Monkey:
    return Monkey(
        items=parse_items(lines[1]),
        operation=parse_operation(lines[2]),
        divisor=parse_divisor(lines[3]),
        true_dest=parse_true_dest(lines[4]),
        false_dest=Parse_false_dest(lines[5]),
    )


def print_round(i: int, monkeys: List[Monkey]):
    print(f"After round {i}, the monkeys are holding items with these worry levels:")
    for index, monkey in enumerate(monkeys):
        print(f"Monkey {index}: {monkey.items}")


def part1(fn: str):
    monkeys = [
        parse_monkey(monkey_lines)
        for monkey_lines in match_into_chunks(
            file_lines(fn), lambda l: l == "", return_match=False
        )
    ]
    # print_round(0, monkeys)
    for round_no in range(20):
        for monkey in monkeys:
            monkey.round(monkeys)
        # print_round(round_no + 1, monkeys)
    inspecteds = sorted([m.inspected for m in monkeys], reverse=True)[:2]
    return math.prod(inspecteds)


def part2(fn: str):
    pass


print(f"Part1 Sample: {part1('day11/sample')}")
print(f"Part1: {part1('day11/input')}")
# print(f"Part2 Sample: {part2('day11/sample')}")
# print(f"Part2: {part2('day11/input')}")
