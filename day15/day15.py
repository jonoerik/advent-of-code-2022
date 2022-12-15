#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import typing

# (x, y)
Point = tuple[int, int]
# List of sensors, and their closest beacons
InputData = list[tuple[Point, Point]]


def load(input_path: Path) -> InputData:
    sensors = []
    with open(input_path) as f:
        while line := f.readline():
            line = line.strip().split(" ")
            sensors.append(((int(line[2][2:-1]), int(line[3][2:-1])), (int(line[8][2:-1]), int(line[9][2:]))))
    return sensors


def dist(a: Point, b: Point):
    """Taxicab distance between a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# (min_x, max_x)
RowSpan = tuple[int, int]


def SpanOverlap(a: RowSpan, b: RowSpan) -> typing.Union[RowSpan, None]:
    """If the spans overlap, return a span that covers both areas, otherwise return None"""
    if a[0] <= b[0] <= a[1]:
        return (a[0], max(a[1], b[1]))
    elif a[0] <= b[1] <= a[1]:
        return (min(a[0], b[0]), a[1])
    elif b[0] <= a[0] and b[1] >= a[1]:
        return b
    else:
        return None


def part1(input_data: InputData, row: int) -> int:
    beacons_in_row = len(set([beacon for _, beacon in input_data if beacon[1] == row]))
    covered_regions: list[RowSpan] = []
    for sensor, beacon in input_data:
        d = dist(sensor, beacon)
        d_in_row = d - abs(sensor[1] - row)
        if d_in_row >= 0:
            covered_regions.append((sensor[0] - d_in_row, sensor[0] + d_in_row))

    discrete_covered_regions: list[RowSpan] = []  # Regions with no overlap
    while covered_regions:
        reg_a = covered_regions.pop(0)
        for reg_b in covered_regions:
            if overlap := SpanOverlap(reg_a, reg_b):
                covered_regions.remove(reg_b)
                covered_regions.append(overlap)
                break
        else:
            discrete_covered_regions.append(reg_a)

    return sum([maxx - minx + 1 for minx, maxx in discrete_covered_regions]) - beacons_in_row


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
        print(part1(data, 2000000))
    else:  # part2
        print(part2(data))
