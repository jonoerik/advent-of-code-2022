#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import string


def load(input_path: Path) -> list[list[str]]:
    rucksacks = []
    with open(input_path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            rucksacks.append(list(line))
    return rucksacks


def part1(rucksacks: list[list[str]]) -> int:
    return sum([string.ascii_letters.find((set(rucksack[:len(rucksack) // 2]) & set(rucksack[len(rucksack) // 2:])).pop()) + 1 for rucksack in rucksacks])


def part2(rucksacks: list[list[str]]) -> int:
    pass  # TODO


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
