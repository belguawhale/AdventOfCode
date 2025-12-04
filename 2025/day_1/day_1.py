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

inp = parse_file("input.txt")
print(part_1(inp))


def part_2(rotations: List[int], debug=False):
    num_clicks = 0
    dial = Dial()
    for rotation in rotations:
        if debug:
            print(f"num_clicks {num_clicks} dial {dial.num} rotation {rotation}")
        if rotation > 0:
            # e.g. rotation to 234 is 2 clicks + new position of 34
            # e.g. rotation to 300 is 3 clicks + new position of 0
            num_clicks += (rotation + dial.num) // Dial.DIAL_SIZE
        else:
            # mirror dial state and rotation, then count in the positive direction - integer division doesn't count certain 0 crossings in the negative direction
            mirrored_dial = (Dial.DIAL_SIZE - dial.num) % Dial.DIAL_SIZE
            num_clicks += (mirrored_dial - rotation) // Dial.DIAL_SIZE
        dial.rotate(rotation)
    if debug:
        print(f"FINAL num_clicks {num_clicks} dial {dial.num}")
    return num_clicks


print(part_2(example, debug=True))
print(part_2(inp))

# should click once on 50 (dial: 0), once on 100, twice on +/- 200
test_cases = [
    [[50, 100, -200], 4],
    [[50, 100, 200], 4],
    [[-50], 1],
    [[50], 1],
    [[50, 75, 25], 2],
    [[-50, -75, -25], 2],
    [[49, 2, -2, 1], 3],
    [[-49, -2, 2, -1], 3],
]


def test(cases):
    for inp, expected in cases:
        actual = part_2(inp)
        if actual == expected:
            print(f"+ correct {inp}")
        else:
            print(f"- incorrect {inp}, got {actual}, expected {expected}")
            part_2(inp, debug=True)


test(test_cases)
