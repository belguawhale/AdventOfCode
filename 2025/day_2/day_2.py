from typing import List, Tuple
import math

Range = Tuple[int, int]


def parse_file(file: str):
    ranges: List[Range] = []
    with open(file, "r") as f:
        str_ranges = f.read().split(",")
        for r in str_ranges:
            left, right = r.split("-")
            ranges.append((int(left), int(right)))
    return ranges


# here's a thought, a num of length 2k with repeated digits
# can be written as (10^k + 1) * (a num with k digits)
# e.g. 1234 * 10001 = 12341234
# so for each range, we first preprocess + split them so start and end point are the same # of digits.
#   note each range is an independent subproblem
# discard ranges with odd # of digits
# then we can compute # of multiples of our magic number that exist in the range.
ProcessedRange = Tuple[int, int, int]


def determine_invalid_ids(r: ProcessedRange) -> List[int]:
    left, right, k = r

    magic = 10**k + 1
    first_invalid_above_left = math.ceil(left / magic) * magic
    return list(range(first_invalid_above_left, right + 1, magic))


def process_range(r: Range) -> List[ProcessedRange]:
    left, right = r
    processed_ranges = []

    while left < right:
        num_digits = math.floor(math.log10(left)) + 1
        max_in_range = 10**num_digits - 1
        # print(
        #     f"left {left} right {right} num_digits {num_digits} max_in_range {max_in_range}"
        # )
        if num_digits % 2 == 0:
            # Skip ranges of odd # of digits
            processed_ranges.append((left, min(max_in_range, right), num_digits // 2))
        left = max_in_range + 1
    return processed_ranges


def process_ranges(ranges: List[Range]) -> List[ProcessedRange]:
    processed_ranges = []
    for r in ranges:
        processed_r = process_range(r)
        processed_ranges.extend(processed_r)
    return processed_ranges


def part_1(ranges: List[Range], debug=False):
    total = 0
    processed_ranges = process_ranges(ranges)
    if debug:
        print(f"processed_ranges {processed_ranges}")
    for r in processed_ranges:
        total += sum(determine_invalid_ids(r))
    return total


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [[(11, 22)], 33],  # 11, 22
    [[(95, 115)], 99],  # 99
    [[(1188511880, 1188511890)], 1188511885],  # 1188511885
    [[(1698522, 1698528)], 0],  # no invalid
    [parse_file("input_example.txt"), 1227775554],
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

# For part 2, we can do a similar approach!
# d * 11, d * 111, d * 1111, etc. are 1 digit d repeated
# dd * 101, dd * 10101, dd * 1010101 etc. are 2 digits dd repeated
# When k digits repeat m times, the magic number M_{k,m} = M_{k, m-1} * 10^k + 1


def calc_magic(k, m):
    if m == 1:
        return 1
    return calc_magic(k, m - 1) * 10**k + 1


def determine_invalid_ids_2(r: ProcessedRange) -> List[int]:
    # hacky data model change, third param in ProcessedRange is now just our magic number
    left, right, magic = r

    first_invalid_above_left = math.ceil(left / magic) * magic
    return list(range(first_invalid_above_left, right + 1, magic))


def process_range_2(r: Range) -> List[ProcessedRange]:
    left, right = r
    processed_ranges = []

    while left < right:
        num_digits = math.floor(math.log10(left)) + 1
        max_in_range = 10**num_digits - 1
        # print(
        #     f"left {left} right {right} num_digits {num_digits} max_in_range {max_in_range}"
        # )
        for divisor in range(1, num_digits):
            if num_digits % divisor == 0:
                # Only include ranges that are a multiple of a repeating group size
                to_add = (
                    left,
                    min(max_in_range, right),
                    calc_magic(divisor, num_digits // divisor),
                )
                # print(f"adding {to_add}")
                processed_ranges.append(to_add)
        left = max_in_range + 1
    return processed_ranges


def process_ranges_2(ranges: List[Range]) -> List[ProcessedRange]:
    processed_ranges = []
    for r in ranges:
        processed_r = process_range_2(r)
        processed_ranges.extend(processed_r)
    return processed_ranges


def part_2(ranges: List[Range], debug=False):
    processed_ranges = process_ranges_2(ranges)
    unique_invalid_ids = set()
    if debug:
        print(f"processed_ranges {processed_ranges}")
    for r in processed_ranges:
        invalid_ids = determine_invalid_ids_2(r)
        if debug:
            print(f"invalid_ids: {invalid_ids}")
        unique_invalid_ids |= set(invalid_ids)
    return sum(unique_invalid_ids)


print(part_2(example))
print(part_2(inp))

test_cases_part_2 = [
    [[(11, 22)], 33],  # 11, 22
    [[(95, 115)], 210],  # 99, 111
    [[(1188511880, 1188511890)], 1188511885],  # 1188511885
    [[(1698522, 1698528)], 0],  # no invalid
    [parse_file("input_example.txt"), 4174379265],
]

test(test_cases_part_2, part_2)
