from typing import List, Tuple, Set, Dict
import numpy as np
from collections import deque
import math
import re
from dataclasses import dataclass
import heapq
import string
import pdb


# num_lights, target_state, buttons, joltage_reqs
Machine = Tuple[int, int, List[int], List[int]]
InputType = List[Machine]


def parse_file(file: str) -> InputType:
    machines = []
    with open(file, "r") as f:
        for line in f:
            state, *buttons, joltage = line.strip().split(" ")
            target_state_str = state.strip("[]").replace(".", "0").replace("#", "1")
            num_lights = len(target_state_str)
            button_vals = []
            for button in buttons:
                button_val = 0
                for light in button.strip("()").split(","):
                    # note button i correponds to the i+1th bit which is 1 << (n-i-1)
                    button_val |= 1 << (num_lights - int(light) - 1)
                button_vals.append(button_val)
            joltage_reqs = [int(j) for j in joltage.strip("{}").split(",")]
            machines.append(
                (num_lights, int(target_state_str, 2), button_vals, joltage_reqs)
            )
    return machines


def process_machine(machine: Machine, debug=False) -> int:
    num_lights, target_state, buttons, _ = machine
    distances = {}
    cur_distance = 0
    to_process = deque([(0, 0)])
    while to_process:
        state, cur_distance = to_process.popleft()
        for button in buttons:
            next_state = state ^ button
            if next_state in distances:
                # already visited
                continue
            next_distance = cur_distance + 1
            distances[next_state] = next_distance
            if next_state == target_state:
                return next_distance
            to_process.append((next_state, next_distance))
    raise RuntimeError("did not reach target state")


def part_1(inp: InputType, debug=False):
    # idea: machine state is like a bitstring with 0 being off and 1 being on.
    # each button does an xor with machine state, where 1 toggles a light at index i and 0 leaves it
    # use iterated bfs to determine the shortest path from the 0 state to each machine state, until we find the target state
    total = 0
    for machine in inp:
        total += process_machine(machine, debug)
    return total


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example))

inp = parse_file("input.txt")
print(part_1(inp))

test_cases_part_1 = [
    [[example[0]], 2],
    [[example[1]], 3],
    [[example[2]], 2],
    [parse_file("input_example.txt"), 7],
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

print("===== Part 2 =====")

# num_lights, buttons, joltage_reqs
CounterState = np.typing.NDArray[np.int16]
Machine2 = Tuple[int, List[CounterState], CounterState]
InputType2 = List[Machine2]


def parse_file2(file: str) -> InputType2:
    machines = []
    with open(file, "r") as f:
        for line in f:
            state, *buttons, joltage = line.strip().split(" ")
            target_state_str = state.strip("[]").replace(".", "0").replace("#", "1")
            num_lights = len(target_state_str)
            button_vals = []
            for button in buttons:
                vals = np.zeros(num_lights, dtype=np.int16)
                for light in button.strip("()").split(","):
                    vals[int(light)] = 1
                button_vals.append(vals)
            joltage_reqs = np.array(
                [int(j) for j in joltage.strip("{}").split(",")], dtype=np.int16
            )
            machines.append((num_lights, button_vals, joltage_reqs))
    return machines


def determine_max_coefficient(button: CounterState, target: CounterState) -> int:
    # determines the maximum number of times button can go into target
    # button is effectively a mask here
    return min(c for i, c in enumerate(target) if button[i])


def process_machine2(machine: Machine2, debug=False) -> int:
    num_counters, buttons, joltage_reqs = machine
    num_buttons = len(buttons)

    # Each button is like a vector in a spanning set for num_counters-D space.
    # A solution is a linear combination of buttons that equal the joltage req
    # with the constraint that
    # 1. each coefficient is non-negative, and
    # 2. we optimize for the smallest sum of coefficients

    # max num_counters is about 10, max joltage reqs is about 300.

    # greedy attempt with backtracking: sort buttons decreasing by most counters affected,
    # then try to maximize the amount of earlier buttons used.
    # we will dfs since the max depth is num_counters = 10.
    reordered_buttons = sorted(
        enumerate(buttons), key=lambda ebs: sum(ebs[1]), reverse=True
    )
    new_button_to_old_button = np.array(
        [i for i, _ in reordered_buttons], dtype=np.int16
    )
    new_buttons = np.array([new for _, new in reordered_buttons], dtype=np.int16)

    if debug:
        print("sorted buttons", new_buttons, new_button_to_old_button)

    button_counts = np.zeros(num_buttons, dtype=np.int16)

    if debug:
        pdb.set_trace()

    # We're assuming greedy solution is optimal
    # Though I suspect it won't necessarily hold when multiple buttons have the same size

    # create recursive for loop with depth new_buttons
    def recurse(index: int):
        remaining_joltage_reqs = joltage_reqs - (button_counts @ new_buttons)
        max_coeff_for_index = determine_max_coefficient(
            new_buttons[index], remaining_joltage_reqs
        )
        if debug:
            print("===== init index", index, "=====")
            print("remaining", remaining_joltage_reqs)
            print("max coeff", max_coeff_for_index)

        for n in range(max_coeff_for_index, -1, -1):
            button_counts[index] = n
            remaining_joltage_reqs = joltage_reqs - (button_counts @ new_buttons)
            if debug:
                print(
                    "Button counts", button_counts, "Remaining", remaining_joltage_reqs
                )
            if not remaining_joltage_reqs.any():
                print("FOUND COMBO", button_counts)
                return "halt"
            if index + 1 < num_buttons:
                ret = recurse(index + 1)
                if ret == "halt":
                    return ret

    recurse(0)
    return sum(button_counts)


def part_2(inp: InputType2, debug=False):
    total = 0
    for machine in inp:
        total += process_machine2(machine, debug)
    return total


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))


test_cases_part_2 = [
    [[[1, [np.array([1])], np.array([2])]], 2],
    [[[2, [np.array([1, 0]), np.array([0, 1])], np.array([1, 1])]], 2],
    [[example[0]], 10],
    [[example[1]], 12],
    [[example[2]], 11],
    [parse_file2("input_example.txt"), 33],
]


test(test_cases_part_2, part_2)
