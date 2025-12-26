from typing import List, Tuple, Set
import math
import re
from dataclasses import dataclass


@dataclass
class Point3D:
    x: int
    y: int
    z: int

    def distance_sq(self, other: Point3D):
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


InputType = List[Point3D]


def parse_file(file: str) -> InputType:
    points = []
    with open(file, "r") as f:
        for line in f:
            x, y, z = line.strip().split(",")
            points.append(Point3D(int(x), int(y), int(z)))
    return points


def part_1(inp: InputType, num_connections: int, debug=False):
    n = len(inp)
    adjacency_matrix = [[0] * n for _ in range(n)]
    # each node will belong to a circuit id
    circuits = [0] * n
    next_circuit = 1

    # terrible but the idea is there
    # ideally we'd use a fixed length priority queue (heap?) to track the
    # shortest num_connections distances.
    sorted_adjacencies = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = inp[i].distance_sq(inp[j])
            adjacency_matrix[i][j] = dist
            sorted_adjacencies.append((dist, i, j))
    sorted_adjacencies.sort(key=lambda a: a[0])

    for _, i, j in sorted_adjacencies[:num_connections]:
        if debug:
            print("joining", i, j, end="")
        existing_circuit = max(circuits[i], circuits[j])
        # join boxes at indexes i and j
        if existing_circuit:
            if debug:
                print(" adding to existing circuit", existing_circuit)
            if circuits[i] == 0 or circuits[j] == 0:
                # one node disconnected, join with existing circuit
                circuits[i] = circuits[j] = existing_circuit
            else:
                # both nodes already part of different circuits
                # need to move all nodes from one circuit into the other
                canonical_circuit = min(circuits[i], circuits[j])
                for idx, circuit in enumerate(circuits):
                    if circuit == existing_circuit:
                        circuits[idx] = canonical_circuit
        else:
            if debug:
                print(" adding to new circuit", next_circuit)
            circuits[i] = circuits[j] = next_circuit
            next_circuit += 1
    # determine circuit sizes by id
    circuit_sizes = [0] * n
    for c in circuits:
        circuit_sizes[c] += 1

    if debug:
        print(circuits)
        print(circuit_sizes)
        circuit_contents = [[] for _ in range(n)]
        for i, c in enumerate(circuits):
            circuit_contents[c].append(i)
        for i, contents in enumerate(circuit_contents):
            if contents:
                print("circuit", i, ":", contents, [inp[node] for node in contents])
    a, b, c, *_ = sorted(circuit_sizes[1:], reverse=True)
    return a * b * c


print("===== Part 1 =====")
example = parse_file("input_example.txt")
print(part_1(example, 10))

inp = parse_file("input.txt")
print(part_1(inp, 1000))

test_cases_part_1 = [
    [parse_file("input_example.txt"), 40],
]


def test(cases, fn):
    for inp, expected in cases:
        actual = fn(inp)
        if actual == expected:
            print(f"+ correct {inp}")
        else:
            print(f"- incorrect {inp}, got {actual}, expected {expected}")
            fn(inp, debug=True)


test(test_cases_part_1, lambda inp, debug=False: part_1(inp, 10, debug))

exit()

print("===== Part 2 =====")

parse_file2 = parse_file


def part_2(inp: InputType, debug=False):
    pass


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file2("input_example.txt"), 40],
]

test(test_cases_part_2, part_2)
