from dataclasses import dataclass, field
from typing import Dict, Generator, Iterator, Optional, Tuple

from utils import file_lines, match_into_chunks


@dataclass
class File:
    parent: "Directory"
    name: str
    size: int


@dataclass
class Directory:
    parent: Optional["Directory"]
    name: str
    dirs: Dict[str, "Directory"] = field(default_factory=lambda: {})
    files: Dict[str, File] = field(default_factory=lambda: {})


def directory_structure(lines: Iterator[str]) -> Directory:
    root = Directory(parent=None, name="root")
    cwd = root

    for chunk in match_into_chunks(lines, lambda s: s.startswith("$ ")):
        command, result = chunk[0], chunk[1:]
        if command.startswith("$ cd "):
            target_dir = command[5:]
            if target_dir == "..":
                assert cwd.parent is not None
                cwd = cwd.parent
            elif target_dir == "/":
                cwd = root
            else:
                assert target_dir in cwd.dirs.keys()
                cwd = cwd.dirs[target_dir]
        elif command.startswith("$ ls"):
            for list_item in result:
                if list_item.startswith("dir "):
                    dirname = list_item[4:]
                    assert dirname not in cwd.dirs.keys()
                    cwd.dirs[dirname] = Directory(parent=cwd, name=dirname)
                else:
                    size, filename = list_item.split(" ")
                    assert filename not in cwd.files.keys()
                    cwd.files[filename] = File(
                        parent=cwd, name=filename, size=int(size)
                    )

    return root


def size(dir: Directory) -> int:
    return sum(size(subdir) for subdir in dir.dirs.values()) + sum(
        f.size for f in dir.files.values()
    )


def dir_sizes(dir: Directory) -> Generator[Tuple[Directory, int], None, None]:
    yield (dir, size(dir))
    for subdir in dir.dirs.values():
        yield from dir_sizes(subdir)


def small_dirs(
    dir: Directory, max_size: int = 100000
) -> Generator[Tuple[Directory, int], None, None]:
    for dir, size in dir_sizes(dir):
        if size <= max_size:
            yield (dir, size)


def part1(file_name: str):
    return sum(
        size for sd, size in small_dirs(directory_structure(file_lines(file_name)))
    )


def print_tree(dir: Directory, indent: int = 0, recursive: bool = True):
    print((" " * indent) + f"- {dir.name} (size: {size(dir)})")
    for file in dir.files.values():
        print((" " * (indent + 2)) + f"| {file.name} (size: {file.size})")
    for dir in dir.dirs.values():
        if recursive:
            print_tree(dir, indent + 2, True)
        else:
            print((" " * (indent + 2)) + f"- {dir.name} (size: {size(dir)})")


def part2(file_name: str):
    total_size = 70000000
    total_needed = 30000000

    root = directory_structure(file_lines(file_name))

    size_of_root = size(root)

    free_space = total_size - size_of_root
    needed = total_needed - free_space

    for (dir, s) in sorted(dir_sizes(root), key=lambda e: e[1]):
        if s >= needed:
            return s


print(f"Part1 Sample: {part1('day7/sample')}")
print(f"Part1: {part1('day7/input')}")
print(f"Part2 Sample: {part2('day7/sample')}")
print(f"Part2: {part2('day7/input')}")
