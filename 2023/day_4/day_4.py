import re


def part_1(inp):
    total = 0

    for winning_numbers, have_numbers in inp:
        matching_numbers = set(winning_numbers).intersection(set(have_numbers))
        if matching_numbers:
            total += 2 ** (len(matching_numbers) - 1)
    return total


def part_2(inp):
    num_matching = []
    num_of_each_card = [1] * len(inp)

    for winning_numbers, have_numbers in inp:
        matching_numbers = set(winning_numbers).intersection(set(have_numbers))
        num_matching.append(len(matching_numbers))
    
    print(num_matching)

    for i in range(len(inp)):
        print(num_of_each_card)
        num_copies = num_of_each_card[i]
        for j in range(num_matching[i]):
            num_of_each_card[i+j+1] += num_copies
    return sum(num_of_each_card)

def parse_file(file):
    ret = []
    with open(file, "r") as f:
        inp = f.read().strip()

        for row, line in enumerate(inp.split("\n")):
            winning_str, have_numbers_str = line.split(": ")[1].split(" | ")
            winning_numbers = list(filter(None, winning_str.split(" ")))
            have_numbers = list(filter(None, have_numbers_str.split(" ")))

            ret.append((winning_numbers, have_numbers))

    return ret


inp_example = parse_file("input_example.txt")
print(inp_example)
print(part_1(inp_example))

inp = parse_file("input.txt")
print(part_1(inp))

inp_example2 = parse_file("input_example2.txt")
print(part_2(inp_example2))

print(part_2(inp))
