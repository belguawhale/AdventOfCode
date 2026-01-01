from typing import List, Tuple, Set, Dict
import math
import re
from dataclasses import dataclass
import heapq
import string
import pdb


@dataclass
class Point2D:
    x: int
    y: int
    label: str = ""

    def __str__(self):
        if self.label:
            return f"{self.label}({self.x},{self.y})"
        return repr(self)

    def area(self, other: Point2D):
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


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

print("===== Part 2 =====")

parse_file2 = parse_file


Line = Tuple[int, int, int]


def part_2(inp: InputType, debug=False):
    if debug:
        pdb.set_trace()
    n = len(inp)

    # A rectangle becomes invalid if one of its sides intersects one of the edges of the original shape.
    # for horizontal side (a, y), (b, y), we check all vertical edges between a and b if endpoints are above y and below y.
    # and vice versa.
    # we preprocess the input, storing horizontal and vertical edges. sort horizontal by y pos and vertical by x pos.
    # but what if an edge has one of its endpoints on a side of a rectangle?
    # if the edge points into the rectangle, then it must cut out some area from the rectangle and invalidate it.
    #   (one side of the edge is inside and one side of the edge is outside the original shape)
    # if the edge points away from the rectangle, the side doesn't matter.
    # for edges originating from a corner of the rectangle, we just need to verify the shape of the corner
    #   corresponds with the shape of the rectangle (e.g. top left to top left)
    #   update: this didn't end up being relevant to our input, but worth noting. we can find the left-most two corners
    #   in O(n) and provide a "shape" of each corner by iterating through each edge of input

    # a line is (pos, start, end)
    horizontal_lines: List[Line] = []
    vertical_lines: List[Line] = []

    is_horizontal = inp[-1].y == inp[0].y
    prev_point = inp[-1]
    for point in inp:
        if is_horizontal:
            sorted_x = (
                (prev_point.x, point.x)
                if prev_point.x < point.x
                else (point.x, prev_point.x)
            )
            horizontal_lines.append((point.y, *sorted_x))
        else:
            sorted_y = (
                (prev_point.y, point.y)
                if prev_point.y < point.y
                else (point.y, prev_point.y)
            )
            vertical_lines.append((point.x, *sorted_y))
        is_horizontal = not is_horizontal
        prev_point = point
    # improvement: use a sorted data structure
    horizontal_lines.sort(key=lambda line: line[0])
    vertical_lines.sort(key=lambda line: line[0])

    corners: Dict[Point2D, str] = {}

    if debug:
        print("horz", horizontal_lines)
        print("vert", vertical_lines)
        print_test_case(inp)

    def check_line(
        lines: List[Line],
        start: int,
        end: int,
        check: int,
        valid_direction_is_less: bool,
    ):
        # improvement: binary search for start + end
        for i, (pos, low, high) in enumerate(lines):
            if pos <= start:
                continue
            if end <= pos:
                break
            if low < check < high:
                # line intersects our rectangle
                return False
            # handle cases where line starts/ends on rectangle edge (e.g. O)
            # O## ###
            # # ### #
            # #     #
            # ######O

            # lines starting on rectangle edge and pointing into the rectangle are invalid
            if valid_direction_is_less and low == check:
                return False
            elif not valid_direction_is_less and check == high:
                return False

        return True

    def check_rect(p1: Point2D, p2: Point2D):
        min_x = min(p1.x, p2.x)
        max_x = max(p1.x, p2.x)
        min_y = min(p1.y, p2.y)
        max_y = max(p1.y, p2.y)

        if debug:
            print(
                "check_rect",
                p1,
                p2,
                "area",
                p1.area(p2),
            )
        if min_x == max_x or min_y == max_y:
            # 1-width rectangles are always valid
            return True
        left = check_line(horizontal_lines, min_y, max_y, min_x, True)
        right = check_line(horizontal_lines, min_y, max_y, max_x, False)
        top = check_line(vertical_lines, min_x, max_x, min_y, True)
        bottom = check_line(vertical_lines, min_x, max_x, max_y, False)

        if debug:
            print(
                "  ",
                left and right and bottom and top,
                "l",
                left,
                "r",
                right,
                "b",
                bottom,
                "t",
                top,
            )
        return left and right and bottom and top

    max_area = 0
    if debug:
        max_rect = inp[0], inp[1]
    for i in range(n):
        for j in range(i + 1, n):
            area = inp[i].area(inp[j])
            if area > max_area and check_rect(inp[i], inp[j]):
                max_area = max(area, max_area)
                if debug:
                    max_rect = inp[i], inp[j]
    if debug:
        print("max_rect", max_rect)
    return max_area


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))


def build_test_case(s: str) -> InputType:
    res: List[Point2D] = []
    row = 0
    col = 0
    for c in s:
        if c.isalpha():
            res.append(Point2D(col, row, c))
        elif c == "\n":
            row += 1
            col = -1
        col += 1
    res.sort(key=lambda p: p.label)
    return res


def print_test_case(inp: List[Point2D]):
    out = [[" "] * 20 for _ in range(20)]
    for i, p in enumerate(inp):
        out[p.y][p.x] = p.label or string.ascii_letters[i]
    rows = []
    for row in out:
        row_str = "".join(row).rstrip()
        rows.append(row_str)
    print("\n".join(rows).strip("\n"))


test_cases_part_2 = [
    [parse_file2("input_example.txt"), 24],
    [
        build_test_case(
            """
             a b
            gh cd
                 
            f   e"""
        ),
        15,
    ],
    [
        build_test_case(
            """
            a b e f
              c d g h
                  j i
            l     k"""
        ),
        21,
    ],
]


test(test_cases_part_2, part_2)
