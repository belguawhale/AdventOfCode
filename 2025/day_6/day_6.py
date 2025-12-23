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

print("===== Part 2 =====")


def parse_file2(file: str) -> InputType:
    # columns are divided based on the index to the left of each operator
    # 123 456
    #  78 9
    # *   +
    #    ^
    with open(file, "r") as f:
        lines = f.readlines()
    op_line = lines.pop().strip("\n")
    ops = re.split("\s+", op_line)

    # determine ending indexes of each column, e.g.
    # 123 234 34 45
    # *   +   *  +
    #   ^   ^  ^  ^
    positions = [group.end() - 3 for group in re.finditer(r"[*+]", op_line)]
    positions = positions[1:] + [len(op_line) - 1]

    rows = []
    for line in lines:
        chunks = []
        start_pos = 0
        for end_pos in positions:
            chunks.append(line[start_pos : end_pos + 1])
            start_pos = end_pos + 2
        rows.append(chunks)
    # print("r", rows)
    cols = list(zip(*rows))
    # print("c", cols)
    vert_nums = [[int("".join(s).strip()) for s in zip(*c)] for c in cols]
    # print("v", vert_nums)
    return list(zip(vert_nums, ops))


def part_2(inp: InputType, debug=False):
    return part_1(inp, debug)


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file2("input_example.txt"), 3263827],
]

test(test_cases_part_2, part_2)
