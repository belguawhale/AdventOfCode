# part 1
from typing import List


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def copy(self):
        return Point(self.x, self.y)

    def is_adjacent(self, other):
        diff = self - other
        return abs(diff.x) <= 1 and abs(diff.y) <= 1

    def unit_manhattan(self):
        ret = Point()
        if abs(self.x) >= 1:
            ret.x = self.x // abs(self.x)
        if abs(self.y) >= 1:
            ret.y = self.y // abs(self.y)
        return ret


def print_rope(rope: List[Point], size=5):
    dimension = size * 2 + 1
    canvas = [["."] * dimension for _ in range(dimension)]
    for i in reversed(range(len(rope))):
        point = rope[i]
        canvas[point.y + size][point.x + size] = str(i)
    canvas[rope[0].y + size][rope[0].x + size] = "H"

    print("\n".join("".join(line) for line in canvas))


def follow(head: Point, tail: Point):
    if head.is_adjacent(tail):
        return tail
    diff = head - tail
    tail_movement = diff.unit_manhattan()
    return tail + tail_movement


DIRECTIONS = {
    "U": Point(0, -1),
    "D": Point(0, 1),
    "L": Point(-1, 0),
    "R": Point(1, 0),
}

tail_visited = {Point(0, 0)}
rope = [Point(0, 0), Point(0, 0)]

with open("input.txt", "r") as f:
    for line in f:
        direction, amount = line.strip().split(" ")
        amount = int(amount)
        for _ in range(amount):
            # print_rope(rope)
            head_movement = DIRECTIONS[direction]
            rope[0] += head_movement

            for i in range(len(rope) - 1):
                rope[i + 1] = follow(rope[i], rope[i + 1])

            tail_visited.add(rope[-1])


print(len(tail_visited))
