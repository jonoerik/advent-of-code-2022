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
    elif a[1] + 1 == b[0]:
        return (a[0], b[1])
    elif b[1] + 1 == a[0]:
        return (b[0], a[1])
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


def clip_coord(r: RowSpan, bounds: RowSpan) -> typing.Union[RowSpan, None]:
    if r[1] < bounds[0] or r[0] > bounds[1]:
        return None
    return (max(r[0], bounds[0]), min(r[1], bounds[1]))


def part2(input_data: InputData, coord_max: int) -> int:
    def find_sensor_gap() -> Point:
        for y in range(0, coord_max + 1):
            covered_regions: list[RowSpan] = []
            for sensor, beacon in input_data:
                d = dist(sensor, beacon)
                d_in_row = d - abs(sensor[1] - y)
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
            discrete_covered_regions.sort(key=lambda r: r[0])
            discrete_covered_regions = [clip_coord(r, (0, coord_max)) for r in discrete_covered_regions]
            discrete_covered_regions = [r for r in discrete_covered_regions if r is not None]
            match discrete_covered_regions:
                case [r]:
                    if r[0] >= 1:
                        assert r[0] == 1
                        return (0, y)
                    elif r[1] < coord_max:
                        assert r[1] == coord_max - 1
                        return (coord_max, y)
                case [r1, r2]:
                    assert r1[1] + 2 == r2[0]
                    assert r1[0] == 0 and r2[1] == coord_max
                    return (r1[1] + 1, y)
                case _:
                    assert False
    beacon = find_sensor_gap()
    return beacon[0] * 4000000 + beacon[1]


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
        print(part2(data, 4000000))
