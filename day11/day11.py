#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from typing import Callable
import operator
import math


class Monkey:
    def __init__(self, items: list[int], op: Callable[[int], int], test: Callable[[int], bool], targets: dict[bool, int]):
        self.items = items
        self.op = op
        self.test = test
        self.targets = targets
        self.inspections_count = 0


# List of instructions (opcode, operand)
InputData = list[Monkey]


def load(input_path: Path) -> InputData:
    monkeys = []
    with open(input_path) as f:
        while True:
            f.readline()  # Monkey number
            starting_items = [int(x) for x in f.readline().strip().split(": ")[-1].split(", ")]
            op_line = f.readline().strip().split(" = ")[-1].split(" ")
            op = (lambda a, o, b: lambda x: {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}[o](x if a == "old" else int(a), x if b == "old" else int(b)))(op_line[0], op_line[1], op_line[2])
            test = (lambda test_val: lambda x: (x % test_val == 0))(int(f.readline().strip().split(" ")[-1]))
            target_true = int(f.readline().strip().split(" ")[-1])
            target_false = int(f.readline().strip().split(" ")[-1])
            monkeys.append(Monkey(starting_items, op, test, {True: target_true, False: target_false}))
            if not f.readline():
                break
    return monkeys


def part1(input_data: InputData) -> int:
    for _ in range(20):
        for monkey in input_data:
            while monkey.items:
                item = monkey.items.pop(0)
                item = monkey.op(item)
                item //= 3
                input_data[monkey.targets[monkey.test(item)]].items.append(item)
                monkey.inspections_count += 1
    return math.prod(sorted([m.inspections_count for m in input_data])[-2:])


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
