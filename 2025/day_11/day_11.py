from typing import List, Tuple, Set, Dict
import numpy as np
from collections import deque, Counter
import math
import re
from dataclasses import dataclass
import heapq
import string
import pdb


InputType = Dict[str, List[str]]


def parse_file(file: str) -> InputType:
    output = {}
    with open(file, "r") as f:
        for line in f:
            device, s_outputs = line.strip().split(": ", 1)
            outputs = s_outputs.split(" ")
            output[device] = outputs
    return output


def part_1(inp: InputType, debug=False):
    # inp is a DAG
    num_paths = Counter({"you": 1})
    visited = set()
    queue = deque(["you"])
    while queue:
        curr = queue.popleft()
        if debug:
            print(curr)
            print(queue)
            print(num_paths)
            print()
        for connection in inp[curr]:
            num_paths[connection] += num_paths[curr]
            if connection != "out" and connection not in visited:
                queue.append(connection)
                visited.add(connection)
    return num_paths["out"]


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 5],
]


def test(cases, fn):
    for inp, expected in cases:
        try:
            actual = fn(inp)
        except Exception as e:
            actual = e
        if actual == expected:
            print(f"+ correct {inp}")
        else:
            if isinstance(actual, Exception):
                print(f"- incorrect {inp}, got exception {actual!r}")
            else:
                print(f"- incorrect {inp}, got {actual}, expected {expected}")
            fn(inp, debug=True)


test(test_cases_part_1, part_1)

exit()

print("===== Part 2 =====")

InputType2 = InputType


def parse_file2(file: str) -> InputType2:
    return parse_file(file)


def part_2(inp: InputType2, debug=False):
    pass


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))


test_cases_part_2 = [
    [parse_file2("input_example.txt"), 33],
]


test(test_cases_part_2, part_2)
