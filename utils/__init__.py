from itertools import islice, tee, zip_longest
from typing import Callable, Dict, Generator, Iterator, List, Tuple, TypeVar

T = TypeVar("T")


def character_pairs(str: str) -> Generator[str, None, None]:
    for i in range(len(str) - 1):
        yield str[i : i + 2]


def bin_to_dec(lst: List[str]) -> int:
    return int("".join(lst), 2)


def hex_to_bin_str(str: str) -> str:
    bin_str = ""
    for hex_digit in str:
        bin_str += f"{int(hex_digit, 16):0>4b}"
    return bin_str


def file_lines(fn: str) -> Generator[str, None, None]:
    with open(fn, "rt") as f:
        for line in f.read().splitlines():
            yield line


def all_pairs(lst: List[T]) -> Generator[Tuple[T, T], None, None]:
    for p1 in lst:
        for p2 in lst:
            if p1 != p2:
                yield (p1, p2)


def take(iterator: Iterator[T], n: int) -> Generator[T, None, None]:
    for item in islice(iterator, n):
        yield item


def take_while(iterator: Iterator[T], check: Callable[[T], bool]):
    try:
        while True:
            item = next(iterator)
            if check(item):
                yield item
            else:
                return
    except StopIteration:
        pass


def match_into_chunks(
    iterator: Iterator[T], match: Callable[[T], bool], return_match: bool = True
) -> Generator[List[T], None, None]:
    chunk = [next(iterator)]
    for elem in iterator:
        if match(elem):
            yield chunk
            chunk = [elem] if return_match else []
        else:
            chunk.append(elem)
    yield chunk


def chunks(
    iterator: Iterator[T], chunk_size: int, fillvalue: T
) -> Generator[Tuple[T, ...], None, None]:
    args = [iter(iterator)] * chunk_size
    for chunk in zip_longest(*args, fillvalue=fillvalue):
        yield chunk


def consume(iterator: Iterator) -> None:
    [_ for _ in iterator]


def has_elements(iterator: Iterator) -> Tuple[bool, Iterator]:
    iterator, copy = tee(iterator)
    return any(True for _ in copy), iterator


def draw_coordinates(coords: Dict[Tuple[int, int], str]) -> str:
    min_x = min(coords.keys(), key=lambda p: p[0])[0]
    max_x = max(coords.keys(), key=lambda p: p[0])[0]
    min_y = min(coords.keys(), key=lambda p: p[1])[1]
    max_y = max(coords.keys(), key=lambda p: p[1])[1]

    print(f"Coords: {coords}, max_x: {max_x}, min_x: {min_x}")
    out = ""

    for x in range(max_x, min_x - 1, -1):
        for y in range(min_y, max_y + 1):
            coord = coords.get((x, y), None)
            out += coord if coord is not None else "."
        out += "\n"

    return out
