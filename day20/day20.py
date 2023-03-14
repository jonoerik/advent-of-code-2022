#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

InputData = list[int]


def load(input_path: Path) -> InputData:
    with open(input_path) as f:
        return [int(line.strip()) for line in f.readlines()]


def part1(input_data: InputData) -> int:
    # Annotate each data element with its initial index in the input data.
    data = list(enumerate(input_data))
    for i in range(len(data)):
        val = input_data[i]
        # Current index of the item to be moved.
        current_index = data.index((i, val))
        # Wrap numbers in range [1, len(data)].
        new_index = ((current_index + val - 1) % (len(data) - 1)) + 1
        del data[current_index]
        data.insert(new_index, (i, val))
    data = [elem[1] for elem in data]
    zero_index = data.index(0)
    return sum([data[(zero_index + i) % len(data)] for i in [1000, 2000, 3000]])


def part2(input_data: InputData) -> int:
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
