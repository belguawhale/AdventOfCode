from typing import List, Tuple
import math

InputRange = Tuple[int, int]

InputType = Tuple[List[InputRange], List[int]]


def parse_file(file: str) -> InputType:
    ranges = []
    ingredients = []

    with open(file, "r") as f:
        while line := f.readline().strip():
            id_range = line.split("-")
            ranges.append((int(id_range[0]), int(id_range[1])))
        while line := f.readline().strip():
            ingredients.append(int(line))
    return ranges, ingredients


def merge_ranges(ranges: List[InputRange]) -> List[InputRange]:
    return ranges


def part_1(inp: InputType, debug=False):
    ranges, ingredients = inp
    count = 0
    for ing in ingredients:
        # brute force sol works lol
        for r in ranges:
            if ing in range(r[0], r[1] + 1):
                count += 1
                break
    return count


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 3],
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
exit()

example = parse_file("input_example.txt")
print(part_2(example))

inp = parse_file("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file("input_example.txt"), 43],
]
