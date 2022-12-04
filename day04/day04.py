#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import string
import operator
import functools

InputData = list[tuple[tuple[int, int], tuple[int, int]]]


def load(input_path: Path) -> InputData:
    pairs = []
    with open(input_path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip().split(",")
            pairs.append(tuple([tuple([int(range_half) for range_half in pair_member.split("-")]) for pair_member in line]))
    return pairs


def part1(pairs: InputData) -> int:
    count = 0
    for a, b in pairs:
        if (a[0] >= b[0] and a[1] <= b[1]) or (b[0] >= a[0] and b[1] <= a[1]):
            count += 1
    return count


def part2(pairs: InputData) -> int:
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
