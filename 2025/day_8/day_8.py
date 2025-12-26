from typing import List, Tuple, Set
import math
import re
from dataclasses import dataclass
import heapq


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
    # each node will belong to a circuit id
    circuits = [0] * n
    next_circuit = 1

    # this is a maxheap with length num_connections.
    # we pushpop each (distance, i, j) so it maintains the n smallest distances
    # this is O(n^2 log c), can prob reduce the n^2 part by preprocessing points?
    # we don't care about the order so no need to sort after
    n_smallest_adjacencies = [(1e9, 0, 0)] * num_connections
    for i in range(n):
        for j in range(i + 1, n):
            dist = inp[i].distance_sq(inp[j])
            heapq.heappushpop_max(n_smallest_adjacencies, (dist, i, j))

    for _, i, j in n_smallest_adjacencies:
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

print("===== Part 2 =====")

parse_file2 = parse_file


def part_2(inp: InputType, debug=False):
    n = len(inp)
    # each node will belong to a circuit id
    circuits = [0] * n
    next_circuit = 1

    # this is now a minheap since order matters
    # simply push each (distance, i, j), then pop_min until circuit condition is reached

    # O(n^2 log n) for construction, can prob reduce the n^2 part by preprocessing points?
    # O(n^2 log n) worst case looping over all adjacencies, in practise not sure how to prove we'll exit earlier
    # circuit merging is currently O(n) which is not great

    # dist, i, j
    adjacency_minheap: List[Tuple[int, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = inp[i].distance_sq(inp[j])
            heapq.heappush(adjacency_minheap, (dist, i, j))

    # faster way to lookup what nodes are in a circuit
    circuit_sets: List[Set[int]] = [set(range(n))] + [set() for _ in range(n)]
    while adj := heapq.heappop(adjacency_minheap):
        _, i, j = adj
        existing_circuit = max(circuits[i], circuits[j])
        # join boxes at indexes i and j
        if debug:
            print("joining", inp[i], inp[j], end="")
        if circuits[i] == circuits[j] == 0:
            if debug:
                print(" adding to new circuit", next_circuit)
            circuits[i] = circuits[j] = next_circuit
            circuit_sets[next_circuit].add(i)
            circuit_sets[next_circuit].add(j)
            next_circuit += 1
        elif circuits[i] == circuits[j]:
            if debug:
                print(" already part of existing circuit", existing_circuit)
            continue
        else:
            canonical_circuit = min(circuits[i], circuits[j])
            existing_circuit = max(circuits[i], circuits[j])
            if canonical_circuit:
                # both nodes part of different circuits
                if debug:
                    print(" merging circuits", existing_circuit, canonical_circuit)

                # move all nodes from one circuit into the other
                for idx in circuit_sets[existing_circuit]:
                    circuits[idx] = canonical_circuit
                circuit_sets[canonical_circuit].update(circuit_sets[existing_circuit])
                circuit_sets[existing_circuit] = set()
            else:
                if debug:
                    print(" adding to existing circuit", existing_circuit)
                # one node disconnected, join with existing circuit
                circuits[i] = circuits[j] = existing_circuit
                circuit_sets[existing_circuit].add(i)
                circuit_sets[existing_circuit].add(j)

            changed_circuit = canonical_circuit or existing_circuit
            if len(circuit_sets[changed_circuit]) == n:
                break

        if debug:
            print("", "circuits", circuits)
    return inp[i].x * inp[j].x


example = parse_file2("input_example.txt")
print(part_2(example))

inp = parse_file2("input.txt")
print(part_2(inp))

test_cases_part_2 = [
    [parse_file2("input_example.txt"), 25272],
]

test(test_cases_part_2, part_2)
