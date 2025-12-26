from typing import List, Tuple, Set
import math
import re
from dataclasses import dataclass
import heapq


@dataclass
class Point2D:
    x: int
    y: int

    def area(self, other: Point2D):
        return abs(self.x - other.x + 1) * abs(self.y - other.y + 1)


InputType = List[Point2D]


def parse_file(file: str) -> InputType:
    points = []
    with open(file, "r") as f:
        for line in f:
            x, y = line.strip().split(",")
            points.append(
                Point2D(
                    int(x),
                    int(y),
                )
            )
    return points


def part_1(inp: InputType, debug=False):
    n = len(inp)
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = inp[i].area(inp[j])
            max_area = max(area, max_area)
    return max_area


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 50],
]


def test(cases, fn):
    for inp, expected in cases:
        actual = fn(inp)
        if actual == expected:
            print(f"+ correct {inp}")
        else:
            print(f"- incorrect {inp}, got {actual}, expected {expected}")
            fn(inp, debug=True)


test(test_cases_part_1, part_1)

exit()

print("===== Part 2 =====")

parse_file2 = parse_file


def part_2(inp: InputType, debug=False):
    pass


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file2("input_example.txt"), 25272],
]

test(test_cases_part_2, part_2)
