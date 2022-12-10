# part 1
num_fully_contained_pairs = 0

with open("input.txt", "r") as f:
    for line in f:
        first_pair, second_pair = line.strip("\n").split(",")

        first_start = int(first_pair.split("-")[0])
        first_end = int(first_pair.split("-")[1])

        second_start = int(second_pair.split("-")[0])
        second_end = int(second_pair.split("-")[1])

        # to fully contain, either we have the ordering 1s 2s 2e 1e or 2s 1s 1e 2e.
        if (
            first_start <= second_start <= second_end <= first_end
            or second_start <= first_start <= first_end <= second_end
        ):
            num_fully_contained_pairs += 1

print(num_fully_contained_pairs)

# part 2
num_overlapping_pairs = 0

with open("input.txt", "r") as f:
    for line in f:
        first_pair, second_pair = line.strip("\n").split(",")

        first_start = int(first_pair.split("-")[0])
        first_end = int(first_pair.split("-")[1])

        second_start = int(second_pair.split("-")[0])
        second_end = int(second_pair.split("-")[1])

        if (
            first_start <= second_start <= first_end
            or first_start <= second_end <= first_end
            or second_start <= first_start <= second_end
            or second_start <= first_end <= second_end
        ):
            num_overlapping_pairs += 1

print(num_overlapping_pairs)
