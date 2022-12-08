#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

# List of rows, data[row][col]
InputData = list[list[int]]


def load(input_path: Path) -> InputData:
    trees: InputData = []
    with open(input_path) as f:
        while line := f.readline().strip():
            trees.append([int(x) for x in list(line)])
    return trees


def scan_row(input_data: InputData, visible: list[list[bool]], row: int):
    cols = len(input_data[0])

    # Left-to-right
    peak_height = input_data[row][0]
    visible[row][0] = True
    for col in range(1, cols):
        if input_data[row][col] > peak_height:
            peak_height = input_data[row][col]
            visible[row][col] = True

    # Right-to-left
    peak_height = input_data[row][cols-1]
    visible[row][cols-1] = True
    for col in range(cols-1, -1, -1):
        if input_data[row][col] > peak_height:
            peak_height = input_data[row][col]
            visible[row][col] = True


def scan_col(input_data: InputData, visible: list[list[bool]], col: int):
    rows = len(input_data)

    # Top-to-bottom
    peak_height = input_data[0][col]
    visible[0][col] = True
    for row in range(1, rows):
        if input_data[row][col] > peak_height:
            peak_height = input_data[row][col]
            visible[row][col] = True

    # Bottom-to-top
    peak_height = input_data[rows-1][col]
    visible[rows-1][col] = True
    for row in range(rows-1, -1, -1):
        if input_data[row][col] > peak_height:
            peak_height = input_data[row][col]
            visible[row][col] = True


def part1(input_data: InputData) -> int:
    rows = len(input_data)
    cols = len(input_data[0])
    visible = [[False for c in range(cols)] for r in range(rows)]

    for row in range(rows):
        scan_row(input_data, visible, row)
    for col in range(cols):
        scan_col(input_data, visible, col)

    return sum([sum([1 if x else 0 for x in row]) for row in visible])


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
