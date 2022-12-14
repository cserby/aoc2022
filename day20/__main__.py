from typing import Iterator, List, Optional

from utils import file_lines


class ElemIterator(Iterator["Elem"]):
    first: "Elem"
    curr: Optional["Elem"]

    def __init__(self, elem: "Elem") -> None:
        super().__init__()
        self.first = elem
        self.curr = None

    def __next__(self) -> "Elem":
        if self.curr == self.first:
            raise StopIteration

        if self.curr is None:
            self.curr = self.first

        curr = self.curr
        self.curr = curr.next
        return curr


class Elem:
    prev: Optional["Elem"]
    next: Optional["Elem"]
    value: int

    def __init__(self, value: int, prev: Optional["Elem"]):
        self.value = value
        self.prev = prev
        self.next = None

    def to_list(self) -> List[int]:
        return [e.value for e in iter(self)]

    def to_elem_list(self) -> List["Elem"]:
        return [e for e in iter(self)]

    def __iter__(self) -> ElemIterator:
        return ElemIterator(self)

    @staticmethod
    def from_file(fn: str, decryption_key: int = 1) -> "Elem":
        lines = iter(list(file_lines(fn)))
        head = Elem(int(next(lines)) * decryption_key, None)
        prev = head
        for l in lines:
            prev.next = Elem(int(l) * decryption_key, prev)
            prev = prev.next
        prev.next = head
        head.prev = prev
        return head

    def mix(self, list_length: int) -> None:
        if self.value == 0:
            return

        prev = self.prev
        next = self.next

        assert prev is not None
        assert next is not None

        prev.next = next
        next.prev = prev

        curr = self

        if self.value > 0:
            curr = self.nth(self.value % (list_length - 1))
            self.next = curr.next
            self.prev = curr
            curr.next = self
            assert self.next is not None
            self.next.prev = self
        else:
            curr = self.nth(self.value % (list_length - 1) + 1)
            self.prev = curr.prev
            self.next = curr
            assert curr.prev is not None
            curr.prev.next = self
            curr.prev = self

    def nth(self, n: int) -> "Elem":
        if n == 0:
            return self
        elif n > 0:
            curr = self
            for _ in range(n):
                assert curr.next is not None
                curr = curr.next
            return curr
        else:
            curr = self
            for _ in range(abs(n)):
                assert curr.prev is not None
                curr = curr.prev
            return curr


def part1(fn: str) -> int:
    ring = Elem.from_file(fn)
    orig_order = ring.to_elem_list()
    zero: Optional[Elem] = None

    for e in orig_order:
        e.mix(len(orig_order))
        if e.value == 0:
            zero = e

    assert zero is not None
    groove_coords = [zero.nth(n).value for n in [1000, 2000, 3000]]
    print(groove_coords)
    return sum(groove_coords)


def part2(fn: str) -> int:
    ring = Elem.from_file(fn, decryption_key=811589153)
    orig_order = ring.to_elem_list()
    zero: Optional[Elem] = None

    for _ in range(10):
        for e in orig_order:
            e.mix(len(orig_order))
            if zero is None and e.value == 0:
                zero = e
        assert zero is not None

    assert zero is not None
    groove_coords = [zero.nth(n).value for n in [1000, 2000, 3000]]
    return sum(groove_coords)


print(f"Part1 Sample: {part1('day20/sample')}")
print(f"Part1: {part1('day20/input')}")
print(f"Part2 Sample: {part2('day20/sample')}")
print(f"Part2: {part2('day20/input')}")
