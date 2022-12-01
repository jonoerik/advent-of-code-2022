#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path


def load(input_path: Path) -> list[list[int]]:
    elf = []
    elves = []
    with open(input_path) as f:
        while True:
            line = f.readline()
            if not line or not line.strip():
                # EOF or blank line
                elves.append(elf)
                elf = []
                if not line:
                    # EOF
                    break
            line = line.strip()
            if line:
                elf.append(int(line))
    return elves


def part1(elves: list[list[int]]) -> int:
    return max([sum(elf) for elf in elves])


def part2(elves: list[list[int]]) -> int:
    return sum(sorted([sum(elf) for elf in elves])[-3:])


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
