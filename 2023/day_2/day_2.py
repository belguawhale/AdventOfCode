import re


def part_1(inp, r, g, b):
    total = 0

    for game in inp:
        game_id, rounds = game

        max_r = max_g = max_b = 0

        print("Game", game_id)
        for round in rounds:
            if "red" in round:
                max_r = max(max_r, round["red"])
            if "green" in round:
                max_g = max(max_g, round["green"])
            if "blue" in round:
                max_b = max(max_b, round["blue"])
            print("R", max_r, "G", max_g, "B", max_b)

        if max_r <= r and max_g <= g and max_b <= b:
            total += game_id
    return total


def part_2(inp):
    total = 0

    for game in inp:
        game_id, rounds = game

        max_r = max_g = max_b = 0

        print("Game", game_id)
        for round in rounds:
            if "red" in round:
                max_r = max(max_r, round["red"])
            if "green" in round:
                max_g = max(max_g, round["green"])
            if "blue" in round:
                max_b = max(max_b, round["blue"])
            print("R", max_r, "G", max_g, "B", max_b)

        power = max_r * max_g * max_b
        print("power", power)
        total += power
    return total


def parse_file(file):
    ret = []
    with open(file, "r") as f:
        for line in f:
            clean_line = line.strip("\n")
            if not clean_line:
                continue

            # Game 1: 1 blue, 8 green; 14 green, 15 blue; 3 green, 9 blue; 8 green, 8 blue, 1 red; 1 red, 9 green, 10 blue
            id_string, game_string = clean_line.split(": ")
            game_id = int(id_string[len("Game "):])

            rounds = [dict((colour_amounts.split(" ")[1], int(colour_amounts.split(" ")[0]))
                           for colour_amounts in round_string.split(", ")) for round_string in game_string.split("; ")]

            ret.append((game_id, rounds))
    return ret


inp_example = parse_file("input_example.txt")
print(inp_example)
print(part_1(inp_example, 12, 13, 14))

inp = parse_file("input.txt")
print(part_1(inp, 12, 13, 14))

inp_example2 = parse_file("input_example2.txt")
print(part_2(inp_example2))

print(part_2(inp))
