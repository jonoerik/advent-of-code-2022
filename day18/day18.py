#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

InputData = list[tuple[int, int, int]]


def load(input_path: Path) -> InputData:
    result = []
    with open(input_path) as f:
        while line := f.readline():
            point = tuple([int(x) for x in line.strip().split(",")])
            assert len(point) == 3
            result.append(point)
    return result


def part1(input_data: InputData) -> int:
    exposed_faces = 0
    for cube in input_data:
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            if (cube[0] + dx, cube[1] + dy, cube[2] + dz) not in input_data:
                exposed_faces += 1
    return exposed_faces


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
