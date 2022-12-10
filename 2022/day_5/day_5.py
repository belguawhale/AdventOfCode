# part 1
from io import TextIOWrapper
import re


NUM_COLUMNS = 9

crates = [[] for _ in range(NUM_COLUMNS)]


def read_boxes(f: TextIOWrapper):
    while True:
        line = f.readline().strip("\n")
        if len(line) > 2 and line[1].isdigit():
            # skip blank line under numbers
            f.readline()
            break
        for i in range(NUM_COLUMNS):
            # [N] [C]
            #  *   *
            #  1   5
            content = line[i * 4 + 1]
            if content.isupper():
                # treat spaces as empty
                crates[i].insert(0, content)


with open("input.txt", "r") as f:
    read_boxes(f)

    while f:
        line = f.readline().strip("\n")
        if not line:
            # end of flie
            break

        matches = re.match(r"move (\d+) from (\d+) to (\d+)", line)

        amount = int(matches.group(1))
        # 0-indexing :'(
        source = int(matches.group(2)) - 1
        dest = int(matches.group(3)) - 1

        for _ in range(amount):
            crates[dest].append(crates[source].pop())


print("".join(stack[-1] for stack in crates))

# part 2
crates = [[] for _ in range(NUM_COLUMNS)]

with open("input.txt", "r") as f:
    read_boxes(f)

    while f:
        line = f.readline().strip("\n")
        if not line:
            # end of flie
            break

        matches = re.match(r"move (\d+) from (\d+) to (\d+)", line)

        amount = int(matches.group(1))
        source = int(matches.group(2)) - 1
        dest = int(matches.group(3)) - 1

        crates[dest].extend(crates[source][-amount:])
        crates[source] = crates[source][:-amount]


print("".join(stack[-1] for stack in crates))
