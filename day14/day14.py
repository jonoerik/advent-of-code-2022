#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import itertools

# List of lines, each line a list of points (x, y) from origin in upper-left
InputData = list[list[tuple[int, int]]]


def load(input_path: Path) -> InputData:
    lines = []
    with open(input_path) as f:
        while line := f.readline():
            lines.append([tuple([int(v) for v in point.split(",")]) for point in line.strip().split(" -> ")])
    return lines


def line_points(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    result = [a]
    dx = 0 if a[0] == b[0] else 1 if a[0] < b[0] else -1
    dy = 0 if a[1] == b[1] else 1 if a[1] < b[1] else -1
    assert dx == 0 or dy == 0
    pt = a
    while pt != b:
        pt = (pt[0] + dx, pt[1] + dy)
        result.append(pt)
    return result


def part1(input_data: InputData) -> int:
    minx = min([min([point[0] for point in line]) for line in input_data])
    maxx = max([max([point[0] for point in line]) for line in input_data])
    maxy = max([max([point[1] for point in line]) for line in input_data])
    width = maxx - minx + 1
    height = maxy + 1
    input_data = [[(x - minx, y) for x, y in line] for line in input_data]
    sand_start = (500 - minx, 0)
    cave = [[False for col in range(width)] for row in range(height)]
    for line in input_data:
        if len(line) == 1:
            cave[line[0][1]][line[0][0]] = True
        else:
            for a, b in itertools.pairwise(line):
                for x, y in line_points(a, b):
                    cave[y][x] = True

    sand_count = 0
    while True:
        sand = sand_start
        while True:
            for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
                if sand[0] + dx < 0 or sand[0] + dx >= width or sand[1] + dy > maxy:
                    return sand_count
                elif not cave[sand[1] + dy][sand[0] + dx]:
                    sand = (sand[0] + dx, sand[1] + dy)
                    break
            else:
                break
        cave[sand[1]][sand[0]] = True
        sand_count += 1


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
