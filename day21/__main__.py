from typing import Callable, Dict, List, Optional

from utils import file_lines


class Monkey:
    name: str
    _shout: Optional[float]
    operand: Optional[str]
    _op1: Optional[float]
    _op2: Optional[float]
    observers: List[Callable[[float], None]]

    def __init__(
        self,
        name: str,
        shout: Optional[float],
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
        self.shout = eval(f"{self._op1} {self.operand} {self._op2}")

    @property
    def op1(self) -> Optional[float]:
        return self._op1

    @op1.setter
    def op1(self, op1: float) -> None:
        self._op1 = op1
        if self._op2 is not None:
            self._perform_operation()

    @property
    def op2(self) -> Optional[float]:
        return self._op2

    @op2.setter
    def op2(self, op2: float) -> None:
        self._op2 = op2
        if self._op1 is not None:
            self._perform_operation()

    @property
    def shout(self) -> Optional[float]:
        return self._shout

    @shout.setter
    def shout(self, shout: float) -> None:
        self._shout = shout
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

            def set_op1(op1: float) -> None:
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

            def set_op2(op2: float) -> None:
                self.op2 = op2

            monkey.observers.append(set_op2)

    @staticmethod
    def parse(line: str, monkeys: Dict[str, "Monkey"]) -> Dict[str, "Monkey"]:
        (name, value) = line.split(": ")

        monkey = get_monkey(name, monkeys)

        try:
            shout = float(value)
            monkey.shout = shout
        except ValueError:
            (op1, operand, op2) = value.split(" ")
            monkey.operand = operand
            monkey.op1_monkey = get_monkey(op1, monkeys)
            monkey.op2_monkey = get_monkey(op2, monkeys)

        return monkeys

    def __repr__(self) -> str:
        return f"Monkey(name={self.name}, shout={self.shout}, operation={'?' if self.op1 is None else self.op1} {'?' if self.operand is None else self.operand} {'?' if self.op2 is None else self.op2}, observers={len(self.observers)}"


def get_monkey(name: str, monkeys: Dict[str, Monkey]) -> Monkey:
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


def part1(fn: str) -> int:
    monkeys: Dict[str, Monkey] = dict()

    for l in file_lines(fn):
        Monkey.parse(l, monkeys)

    assert "root" in monkeys.keys()
    root_shout = monkeys["root"].shout
    assert root_shout is not None
    return int(root_shout)


class RootMonkey(Monkey):
    def __init__(
        self, op1_monkey: Optional["Monkey"], op2_monkey: Optional["Monkey"]
    ) -> None:
        super().__init__("root", None, None, None, None)

    def _perform_operation(self) -> None:
        assert self._op1 == self.op2


def part2(fn: str) -> float:
    humn_shout = 3.349136384441e12

    monkeys: Dict[str, Monkey] = dict()

    root: Optional[Monkey] = None
    humn: Optional[Monkey] = None
    for l in file_lines(fn):
        if l.startswith("root"):
            (name, value) = l.split(": ")
            (op1_monkey, _, op2_monkey) = value.split(" ")
            root = get_monkey("root", monkeys)
            root.__class__ = RootMonkey
            root.op1_monkey = get_monkey(op1_monkey, monkeys)
            root.op2_monkey = get_monkey(op2_monkey, monkeys)
            continue
        if l.startswith("humn"):
            humn = get_monkey("humn", monkeys)
            continue

        Monkey.parse(l, monkeys)

    assert root is not None
    assert humn is not None

    humn.shout = humn_shout

    return int(humn_shout)


print(f"Part1 Sample: {part1('day21/sample')}")
print(f"Part1: {part1('day21/input')}")
# print(f"Part2 Sample: {part2('day21/sample')}")
print(f"Part2: {part2('day21/input')}")
