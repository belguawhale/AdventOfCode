# part 1
from tokenize import group


def get_priority(item: str):
    if item.isupper():
        return 27 + ord(item) - ord("A")
    else:
        return 1 + ord(item) - ord("a")


total_priority = 0

with open("input.txt", "r") as f:
    for line in f:
        contents = line.strip("\n")
        compartment_1 = contents[: len(contents) // 2]
        compartment_2 = contents[len(contents) // 2 :]

        common_item = set(compartment_1) & set(compartment_2)

        assert len(common_item) == 1

        total_priority += get_priority(common_item.pop())

print(total_priority)

# part 2
total_priority = 0

with open("input.txt", "r") as f:
    while f:
        group_1 = f.readline().strip("\n")
        if not group_1:
            # reached end of file
            break
        group_2 = f.readline().strip("\n")
        group_3 = f.readline().strip("\n")

        common_item = set(group_1) & set(group_2) & set(group_3)

        assert len(common_item) == 1

        total_priority += get_priority(common_item.pop())

print(total_priority)
