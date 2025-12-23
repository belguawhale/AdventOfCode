from typing import List, Tuple
import math
import re

InputType = List[Tuple[List[int], str]]


def parse_file(file: str) -> InputType:
    nums = []
    ops = []
    with open(file, "r") as f:
        lines = f.readlines()
    ops = re.split(r"\s+", lines.pop().strip())
    for line in lines:
        parsed = re.split(r"\s+", line.strip())
        nums.append([int(n) for n in parsed])

    return list(zip(zip(*nums), ops))


def part_1(inp: InputType, debug=False):
    total = 0
    for nums, op in inp:
        if op == "+":
            total += sum(nums)
        else:
            total += math.prod(nums)
    return total


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 4277556],
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

example = parse_file("input_example.txt")
print(part_2(example))

inp = parse_file("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file("input_example.txt"), 14],
]

test(test_cases_part_2, part_2)
