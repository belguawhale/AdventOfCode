# part 1
from collections import Counter

with open("input.txt", "r") as f:
    message = f.read().strip()

last_4_counter = Counter()

for i, c in enumerate(message):
    if i < 3:
        last_4_counter[c] += 1
    else:
        last_4_counter[c] += 1
        if all(n <= 1 for n in last_4_counter.values()):
            print(i + 1)
            break
        last_4_counter[message[i - 3]] -= 1

# part 2
last_14_counter = Counter()

for i, c in enumerate(message):
    if i < 13:
        last_14_counter[c] += 1
    else:
        last_14_counter[c] += 1
        if all(n <= 1 for n in last_14_counter.values()):
            print(i + 1)
            break
        last_14_counter[message[i - 13]] -= 1
