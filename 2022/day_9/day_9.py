# part 1
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


def print_rope(head: Point, tail: Point, size=5):
    dimension = size * 2 + 1
    canvas = [["."] * dimension for _ in range(dimension)]
    canvas[tail.y + size][tail.x + size] = "T"
    canvas[head.y + size][head.x + size] = "H"

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
head = Point(0, 0)
tail = Point(0, 0)

with open("input.txt", "r") as f:
    for line in f:
        direction, amount = line.strip().split(" ")
        amount = int(amount)
        for _ in range(amount):
            # print_rope(head, tail)
            # print("head", head, "tail", tail, "direction", direction)
            head_movement = DIRECTIONS[direction]
            head += head_movement

            tail = follow(head, tail)
            tail_visited.add(tail)


print(len(tail_visited))
