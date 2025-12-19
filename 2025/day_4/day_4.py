from typing import List, Tuple
import math


def parse_file(file: str):
    with open(file, "r") as f:
        return [l.strip() for l in f]

def part_1(grid: List[List[str]], debug=False):
    height = len(grid)
    width = len(grid[0])
    num_neighbour_paper = [[0] * width for _ in range(height)]
    can_access = 0

    neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x or y]
    for r in range(height):
        for c in range(width):
            if grid[r][c] != "@":
                continue
            # for each paper, add 1 to the count of each of its neighbours
            for dr, dc in neighbours:
                n_r = r + dr
                n_c = c + dc
                if 0 <= n_r < height and 0 <= n_c < width:
                    # in bounds
                    num_neighbour_paper[n_r][n_c] += 1

    # print(num_neighbour_paper)
    for r in range(height):
        for c in range(width):
            if grid[r][c] == "@" and num_neighbour_paper[r][c] < 4:
                can_access += 1
    return can_access


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 13],
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
