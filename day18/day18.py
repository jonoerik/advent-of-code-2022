#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

InputData = set[tuple[int, int, int]]


def load(input_path: Path) -> InputData:
    result = set()
    with open(input_path) as f:
        while line := f.readline():
            point = tuple([int(x) for x in line.strip().split(",")])
            assert len(point) == 3
            result.add(point)
    return result


def part1(input_data: InputData) -> int:
    exposed_faces = 0
    for cube in input_data:
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            if (cube[0] + dx, cube[1] + dy, cube[2] + dz) not in input_data:
                exposed_faces += 1
    return exposed_faces


def part2(input_data: InputData) -> int:
    exposed_faces = set()
    max_x = max(input_data, key=lambda x: x[0])[0]
    min_x = min(input_data, key=lambda x: x[0])[0]
    max_y = max(input_data, key=lambda x: x[1])[1]
    min_y = min(input_data, key=lambda x: x[1])[1]
    max_z = max(input_data, key=lambda x: x[2])[2]
    min_z = min(input_data, key=lambda x: x[2])[2]

    for cube in input_data:
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            face_cube = (cube[0] + dx, cube[1] + dy, cube[2] + dz)
            if face_cube not in input_data:
                exposed_faces.add(face_cube)

    visited = set()
    def cube_exposed(cube: tuple[int, int, int]) -> bool:
        nonlocal visited
        if cube in visited:
            return False
        visited.add(cube)
        if not (min_x <= cube[0] <= max_x and min_y <= cube[1] <= max_y and min_z <= cube[2] <= max_z):
            return True
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            face_cube = (cube[0] + dx, cube[1] + dy, cube[2] + dz)
            if face_cube not in input_data and cube_exposed(face_cube):
                return True

    while exposed_faces:
        visited = set()
        if cube_exposed(exposed_faces.pop()):
            for cube in visited:
                exposed_faces.discard(cube)
        else:
            for cube in visited:
                input_data.add(cube)
                exposed_faces.discard(cube)

    return part1(input_data)


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
