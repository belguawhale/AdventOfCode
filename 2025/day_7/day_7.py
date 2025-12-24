from typing import List, Tuple, Set
import math
import re

InputType = Tuple[int, List[Set[int]]]


def parse_file(file: str) -> InputType:
    splitters = []
    with open(file, "r") as f:
        start = f.readline().index("S")
        for line in f.readlines():
            row = set(m.start() for m in re.finditer(r"\^", line))
            if row:
                splitters.append(row)
    return start, splitters


def part_1(inp: InputType, debug=False):
    start, splitters = inp
    beams = {start}
    num_splits = 0
    for row in splitters:
        split_beams = row.intersection(beams)
        num_splits += len(split_beams)
        beams = beams.difference(split_beams)
        for beam in split_beams:
            beams.add(beam - 1)
            beams.add(beam + 1)
    return num_splits


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 21],
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

parse_file2 = parse_file


def part_2(inp: InputType, debug=False):
    start, splitters = inp
    beams = [0] * 141  # len of input array
    beams[start] = 1

    for row in splitters:
        for s in row:
            num_paths = beams[s]
            beams[s] = 0
            beams[s - 1] += num_paths
            beams[s + 1] += num_paths
    return sum(beams)


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file2("input_example.txt"), 40],
]

test(test_cases_part_2, part_2)
