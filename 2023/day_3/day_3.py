import re


def part_1(inp):
    total = 0

    numbers, symbols = inp

    for number, start_coord in numbers:
        # =====
        # =123= (1, 1) => ((0, 0), (2, 4))
        # =====
        top_left = start_coord[0] - 1, start_coord[1] - 1
        bottom_right = start_coord[0] + 1, start_coord[1] + len(number)

        for _, symbol_coord in symbols:
            if top_left[0] <= symbol_coord[0] <= bottom_right[0] and top_left[1] <= symbol_coord[1] <= bottom_right[1]:
                total += int(number)
                continue
    return total


def part_2(inp):
    total = 0

    numbers, symbols = inp

    for char, symbol_coord in symbols:
        if char != "*":
            # not a gear
            continue

        top_left = symbol_coord[0] - 1, symbol_coord[1] - 1
        bottom_right = symbol_coord[0] + 1, symbol_coord[1] + 1

        adjacent_numbers = []

        for number, number_coord in numbers:
            number_end_coord = number_coord[0], number_coord[1] + \
                len(number) - 1

            if top_left[0] <= number_coord[0] <= bottom_right[0] and top_left[1] <= number_coord[1] <= bottom_right[1] or \
                    top_left[0] <= number_end_coord[0] <= bottom_right[0] and top_left[1] <= number_end_coord[1] <= bottom_right[1]:
                adjacent_numbers.append(number)

        if len(adjacent_numbers) == 2:
            total += int(adjacent_numbers[0]) * int(adjacent_numbers[1])

    return total


def parse_file(file):
    # make a sparse representation of input, save coords of all of the numbers (start coord) and all of the symbols
    numbers = []
    symbols = []
    with open(file, "r") as f:
        inp = f.read().strip()

        # if this is "", we aren't currently parsing a number
        curr_number = ""

        for row, line in enumerate(inp.split("\n")):
            if curr_number:
                # current number finished on previous line, end it
                # .123
                # .    -> ("123", (0, 1))
                numbers.append(
                    (curr_number, (row - 1, len(line) - len(curr_number))))
                curr_number = ""

            for col, char in enumerate(line):
                # . is blank (ends number), digits are numbers, anything else is a symbol (also ends number)
                if char.isdigit():
                    curr_number += char
                else:
                    if curr_number:
                        # end current number
                        # .123$ -> ("123", (0, 1))
                        numbers.append(
                            (curr_number, (row, col - len(curr_number))))
                        curr_number = ""

                    if char != ".":
                        symbols.append((char, (row, col)))

    return numbers, symbols


inp_example = parse_file("input_example.txt")
print(inp_example)
print(part_1(inp_example))

inp = parse_file("input.txt")
print(part_1(inp))

inp_example2 = parse_file("input_example2.txt")
print(part_2(inp_example2))

print(part_2(inp))
