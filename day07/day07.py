#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path


class CdCommand:
    def __init__(self, target: str):
        self.target: str = target


class LsCommand:
    def __init__(self):
        self.files: dict[str, int] = {}
        self.dirs: list[str] = []

    def append_file(self, filename: str, size: int):
        self.files[filename] = size

    def append_dir(self, dirname: str):
        self.dirs.append(dirname)


InputData = list[CdCommand | LsCommand]


def load(input_path: Path) -> InputData:
    commands: InputData = []
    with open(input_path) as f:
        while line := f.readline().strip():
            line = line.split(" ")
            if line[:2] == ["$", "cd"]:
                commands.append(CdCommand(line[2]))
            elif line == ["$", "ls"]:
                commands.append(LsCommand())
            else:
                if line[0] == "dir":
                    commands[-1].append_dir(line[1])
                else:
                    commands[-1].append_file(line[1], int(line[0]))
    return commands


class PuzzleFile:
    def __init__(self, size: int):
        self.size_: int = size

    def size(self) -> int:
        return self.size_


class PuzzleDir:
    def __init__(self):
        self.contents: dict[str, PuzzleDir | PuzzleFile] = {}

    def size(self) -> int:
        return sum([x.size() for x in self.contents.values()])


def BuildFsTree(input_data: InputData) -> PuzzleDir:
    working_dir = "/"
    root = PuzzleDir()

    for cmd in input_data:
        if isinstance(cmd, CdCommand):
            if cmd.target == "/":
                working_dir = "/"
            elif cmd.target == "..":
                working_dir = working_dir[:working_dir.rfind("/")] if working_dir.count("/") > 1 else "/"
            else:
                working_dir += ("/" if working_dir != "/" else "") + cmd.target
        elif isinstance(cmd, LsCommand):
            d = root
            for sd in filter(None, working_dir.split("/")):
                d = d.contents[sd]
            for x in cmd.files.keys():
                d.contents[x] = PuzzleFile(cmd.files[x])
            for x in cmd.dirs:
                d.contents[x] = PuzzleDir()

    return root


def part1(input_data: InputData) -> int:
    root = BuildFsTree(input_data)

    def get_small_dirs(pd: PuzzleDir) -> list[int]:
        l = []
        if (s := pd.size()) <= 100000:
            l.append(s)
        for sd in pd.contents.values():
            if isinstance(sd, PuzzleDir):
                l.extend(get_small_dirs(sd))
        return l

    return sum(get_small_dirs(root))


def part2(input_data: InputData) -> int:
    root = BuildFsTree(input_data)
    space_required = 30000000 - 70000000 + root.size()

    def get_sizes(pd: PuzzleDir) -> list[int]:
        l = [pd.size()]
        for sd in pd.contents.values():
            if isinstance(sd, PuzzleDir):
                l.extend(get_sizes(sd))
        return l

    return next(filter(lambda x: x >= space_required, sorted(get_sizes(root))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-1", "--part1", action="store_true")
    parser.add_argument("-2", "--part2", action="store_true")
    parser.add_argument("input")
    args = parser.parse_args()

    if args.part1 == args.part2:
        sys.exit("Exactly one of --part1 or --part2 must be specified.")

    data = load(Path(args.input))
    if args.part1:
        print(part1(data))
    else:  # part2
        print(part2(data))
