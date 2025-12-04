from typing import List


class Dial:
    num: int
    DIAL_START = 50
    DIAL_SIZE = 100

    def __init__(self):
        self.num = self.DIAL_START

    def rotate(self, amount: int):
        self.num = (self.num + amount) % self.DIAL_SIZE


def parse_file(file: str):
    rotations = []
    with open(file, "r") as f:
        for line in f:
            direction = 1 if line[0] == "R" else -1
            amount = int(line[1:])
            rotations.append(direction * amount)
    return rotations


def part_1(rotations: List[int]):
    num_zeroes = 0
    dial = Dial()
    for rotation in rotations:
        dial.rotate(rotation)
        if dial.num == 0:
            num_zeroes += 1
    return num_zeroes


example = parse_file("input_example.txt")
print(part_1(example))

inp_1 = parse_file("input.txt")
print(part_1(inp_1))
