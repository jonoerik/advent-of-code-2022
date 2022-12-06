#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

InputData = list[str]


def load(input_path: Path) -> InputData:
    with open(input_path) as f:
        return list(f.readline().strip())


def part1(input_data: InputData) -> int:
    for i in range(len(input_data) - 3):
        if len(set(input_data[i:i+4])) == 4:
            return i + 4


def part2(input_data: InputData) -> int:
    for i in range(len(input_data) - 13):
        if len(set(input_data[i:i + 14])) == 14:
            return i + 14


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
