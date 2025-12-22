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


def merge_ranges(ranges: List[InputRange], debug=False) -> List[InputRange]:
    # how to merge ranges together?
    # E.g. 10-14, 12-18, 16-20 => 10-20
    # sort ranges by first num
    # iterate.
    #   if a range's start falls inside the range of one seen before,
    #   extend that range's end point to max(prev_range.end, range.end).
    #   if the new range's end is greater than an existing range's start, also merge them.
    #     this can trigger at most one merge, since total overlaps are filtered out by sorting
    #   invariant is that no ranges in the output array overlap.

    sorted_ranges_by_first = sorted(ranges, key=lambda r: r[0])
    merged_ranges: List[InputRange] = [sorted_ranges_by_first[0]]

    for i in range(1, len(ranges)):
        start, end = sorted_ranges_by_first[i]
        # the start <= m_end check can be made more efficient by using a BST for m_end
        # so determining start <= m_end is O(logn)
        # we know m_start <= start already since we're processing in sorted order
        # updating new_end is also O(logn) to reinsert the updated end
        # so overall O(nlogn), sort O(nlogn) + n*O(logn)

        # EDIT: we don't even need to check all previously merged ranges, just the last merged range
        # since any overlapping intervals would have extended it already
        # was worried about a [1, 2], [3, 4], [2, 7] case but sorting orders it in the best way.

        m_start, m_end = merged_ranges[-1]
        if start <= m_end:
            new_end = max(end, m_end)
            merged_ranges[-1] = (m_start, new_end)
            if debug:
                print((start, end), merged_ranges)
            continue

        merged_ranges.append((start, end))
        if debug:
            print((start, end), merged_ranges)
    return merged_ranges


def part_2(inp: InputType, debug=False):
    ranges = inp[0]
    merged_ranges = merge_ranges(ranges, debug)
    if debug:
        print(merged_ranges)

    count = 0
    for r in merged_ranges:
        count += r[1] - r[0] + 1
    return count


example = parse_file("input_example.txt")
print(part_2(example, True))

inp = parse_file("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file("input_example.txt"), 14],
    [[[[1, 2], [3, 4], [2, 7]], []], 7],
]

test(test_cases_part_2, part_2)
