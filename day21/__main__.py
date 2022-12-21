from typing import Callable, Dict, Iterator, List, Optional

from utils import file_lines


class Monkey:
    name: str
    _shout: Optional[int]
    operand: Optional[str]
    _op1: Optional[int]
    _op2: Optional[int]
    observers: List[Callable[[int], None]]

    def __init__(
        self,
        name: str,
        shout: Optional[int],
        operand: Optional[str],
        op1_monkey: Optional["Monkey"],
        op2_monkey: Optional["Monkey"],
    ) -> None:
        self.name = name
        self.observers = []
        self._shout = shout
        self._op1 = None
        self._op2 = None
        self.operand = operand
        if op1_monkey is not None:
            assert op2_monkey is not None

            self.op1_monkey = op1_monkey
            self.op2_monkey = op2_monkey

    def _perform_operation(self) -> None:
        self.shout = eval(f"int({self._op1} {self.operand} {self._op2})")
        print(
            f"Monkey {self.name} performs operation {self._op1} {self.operand} {self._op2}, and gets {self.shout}"
        )

    @property
    def op1(self) -> Optional[int]:
        return self._op1

    @op1.setter
    def op1(self, op1: int) -> None:
        self._op1 = op1
        if self._op2 is not None:
            self._perform_operation()

    @property
    def op2(self) -> Optional[int]:
        return self._op2

    @op2.setter
    def op2(self, op2: int) -> None:
        self._op2 = op2
        if self._op1 is not None:
            self._perform_operation()

    @property
    def shout(self) -> Optional[int]:
        return self._shout

    @shout.setter
    def shout(self, shout: int) -> None:
        self._shout = shout
        print(f"Monkey {self.name} shouts {shout}")
        for notify in self.observers:
            notify(shout)

    @property
    def op1_monkey(self) -> "Monkey":
        raise NotImplementedError()

    @op1_monkey.setter
    def op1_monkey(self, monkey: "Monkey") -> None:
        if monkey.shout is not None:
            self.op1 = monkey.shout
        else:

            def set_op1(op1: int) -> None:
                print(f"Monkey {self.name} hears {monkey.name} shout {op1} (op1)")
                self.op1 = op1

            monkey.observers.append(set_op1)

    @property
    def op2_monkey(self) -> "Monkey":
        raise NotImplementedError()

    @op2_monkey.setter
    def op2_monkey(self, monkey: "Monkey") -> None:
        if monkey.shout is not None:
            self.op2 = monkey.shout
        else:

            def set_op2(op2: int) -> None:
                print(f"Monkey {self.name} hears {monkey.name} shout {op2} (op2)")
                self.op2 = op2

            monkey.observers.append(set_op2)

    @staticmethod
    def parse(line: str, monkeys: Dict[str, "Monkey"]) -> Dict[str, "Monkey"]:
        (name, value) = line.split(": ")

        def get_monkey(name: str) -> Monkey:
            try:
                return monkeys[name]
            except KeyError:
                monkeys[name] = Monkey(
                    name=name,
                    shout=None,
                    operand=None,
                    op1_monkey=None,
                    op2_monkey=None,
                )
                return monkeys[name]

        monkey = get_monkey(name)

        try:
            shout = int(value)
            monkey.shout = shout
        except ValueError:
            (op1, operand, op2) = value.split(" ")
            monkey.operand = operand
            monkey.op1_monkey = get_monkey(op1)
            monkey.op2_monkey = get_monkey(op2)

        return monkeys

    def __repr__(self) -> str:
        return f"Monkey(name={self.name}, shout={self.shout}, operation={'?' if self.op1 is None else self.op1} {'?' if self.operand is None else self.operand} {'?' if self.op2 is None else self.op2}, observers={len(self.observers)}"


def part1(fn: str) -> int:
    monkeys: Dict[str, Monkey] = dict()

    for l in file_lines(fn):
        Monkey.parse(l, monkeys)

    assert "root" in monkeys.keys()
    root_shout = monkeys["root"].shout
    assert root_shout is not None
    return root_shout


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day21/sample')}")
print(f"Part1: {part1('day21/input')}")
# print(f"Part2 Sample: {part2('day21/sample')}")
# print(f"Part2: {part2('day21/input')}")
