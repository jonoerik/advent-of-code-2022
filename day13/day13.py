#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import typing
from enum import Enum

InputVal = typing.Union[int, "InputList"]
InputList = list[InputVal]
InputData = list[tuple[InputList, InputList]]


def load_line(s: str) -> (InputVal, int):
    """
    Return loaded value, and the number of characters in str that were consumed.
    Could use eval for this, but I've chosen the 'character building' approach.
    """
    if s[0] == "[":
        result = []
        i = 1
        while s[i] != "]":
            x, l = load_line(s[i:])
            result.append(x)
            i += l
            if s[i] == ",":
                i += 1
        i += 1
        return result, i
    else:
        if "," in s and "]" in s:
            l = min(s.index(","), s.index("]"))
        elif "," in s:
            l = s.index(",")
        else:
            l = s.index("]")
        return int(s[:l]), l


def load(input_path: Path) -> InputData:
    pairs = []
    with open(input_path) as f:
        while line := f.readline():
            a = load_line(line.strip())[0]
            assert isinstance(a, list)
            b = load_line(f.readline().strip())[0]
            assert isinstance(b, list)
            pairs.append((a, b))
            f.readline()  # Blank line, or EOF
    return pairs


class OrderingResult(Enum):
    Ordered = 1,
    Unordered = 2,
    Inconclusive = 3,


def order_correct(a: InputVal, b: InputVal) -> OrderingResult:
    match isinstance(a, int), isinstance(b, int):
        case True, True:
            if a < b:
                return OrderingResult.Ordered
            elif a > b:
                return OrderingResult.Unordered
            else:
                return OrderingResult.Inconclusive
        case True, False:
            return order_correct([a], b)
        case False, True:
            return order_correct(a, [b])
        case False, False:
            i = 0
            while True:
                match i < len(a), i < len(b):
                    case True, True:
                        if (sub_result := order_correct(a[i], b[i])) != OrderingResult.Inconclusive:
                            return sub_result
                    case True, False:
                        return OrderingResult.Unordered
                    case False, True:
                        return OrderingResult.Ordered
                    case False, False:
                        return OrderingResult.Inconclusive
                i += 1


def part1(input_data: InputData) -> int:
    return sum([i + 1 for i, (a, b) in enumerate(input_data) if order_correct(a, b) == OrderingResult.Ordered])


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
