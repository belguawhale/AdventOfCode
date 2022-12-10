# part 1
max_sum = 0
curr_sum = 0

with open("input.txt", "r") as f:
    for line in f:
        clean_line = line.strip("\n")
        if clean_line == "":
            max_sum = max(max_sum, curr_sum)
            curr_sum = 0
        else:
            curr_sum += int(clean_line)
print(max_sum)

# part 2
import heapq

elf_sums = [-1, -1, -1]
curr_sum = 0

with open("input.txt", "r") as f:
    for line in f:
        clean_line = line.strip("\n")
        if clean_line == "":
            # push current sum into heap of size 3, then pop the smallest off
            heapq.heappushpop(elf_sums, curr_sum)
            curr_sum = 0
        else:
            curr_sum += int(clean_line)
print(sum(elf_sums))
