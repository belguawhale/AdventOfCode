# part 1
trees = []
with open("input.txt", "r") as f:
    for line in f:
        trees.append(list(map(int, line.strip())))
SIZE = len(trees)
print(SIZE)
print(trees)

visible_down = [[False] * SIZE for _ in range(SIZE)]
visible_right = [[False] * SIZE for _ in range(SIZE)]
visible_up = [[False] * SIZE for _ in range(SIZE)]
visible_left = [[False] * SIZE for _ in range(SIZE)]

for i in range(SIZE):
    prev_down = prev_right = prev_up = prev_left = -1
    for j in range(SIZE):
        if prev_down < trees[j][i]:
            visible_down[j][i] = True
            prev_down = trees[j][i]
        if prev_right < trees[i][j]:
            visible_right[i][j] = True
            prev_right = trees[i][j]
        if prev_up < trees[SIZE - j - 1][i]:
            visible_up[SIZE - j - 1][i] = True
            prev_up = trees[SIZE - j - 1][i]
        if prev_left < trees[i][SIZE - j - 1]:
            visible_left[i][SIZE - j - 1] = True
            prev_left = trees[i][SIZE - j - 1]

total_visible = 0

for i in range(SIZE):
    for j in range(SIZE):
        if (
            visible_down[i][j]
            or visible_right[i][j]
            or visible_up[i][j]
            or visible_left[i][j]
        ):
            total_visible += 1

# import numpy as np

# print(np.array(trees))
# print("down\n", np.array(visible_down))
# print("right\n", np.array(visible_right))
# print("up\n", np.array(visible_up))
# print("left\n", np.array(visible_left))
print(total_visible)

# part 2

# saving this in case we lose internet
"""
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390
Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.
"""

# Looking in a certain direction, we want to find the first tree's position
# that has height greater or equal to the current tree. Then that tree's position - our position
# is the number of trees up to it. Since tree heights are limited to < 10, it's faster to lookup
# position by height than iterate through trees in the reverse direction.
# This lookup table will change dynamically as we look through the trees, so we'll need to build it
# in the opposite direction we look.
# e.g. 2 3 2 2 1 looking right, we build the table starting from the right-most 1 and move left.

visible_from_me_down = [[0] * SIZE for _ in range(SIZE)]
visible_from_me_right = [[0] * SIZE for _ in range(SIZE)]
visible_from_me_up = [[0] * SIZE for _ in range(SIZE)]
visible_from_me_left = [[0] * SIZE for _ in range(SIZE)]

for i in range(SIZE):
    # Position is the value of j
    first_pos_height_down = [0] * 10
    first_pos_height_right = [0] * 10
    first_pos_height_up = [0] * 10
    first_pos_height_left = [0] * 10
    for j in range(SIZE):
        # down
        down_row = SIZE - 1 - j  # reverse order
        down_col = i
        down_size = trees[down_row][down_col]
        closest_pos = max(first_pos_height_down[down_size:])
        visible_from_me_down[down_row][down_col] = j - closest_pos
        first_pos_height_down[down_size] = j
        # right
        right_row = i
        right_col = SIZE - 1 - j  # reverse order
        right_size = trees[right_row][right_col]
        closest_pos = max(first_pos_height_right[right_size:])
        visible_from_me_right[right_row][right_col] = j - closest_pos
        first_pos_height_right[right_size] = j
        # up
        up_row = j  # reverse order
        up_col = i
        up_size = trees[up_row][up_col]
        closest_pos = max(first_pos_height_up[up_size:])
        visible_from_me_up[up_row][up_col] = j - closest_pos
        first_pos_height_up[up_size] = j
        # left
        left_row = i
        left_col = j  # reverse order
        left_size = trees[left_row][left_col]
        closest_pos = max(first_pos_height_left[left_size:])
        visible_from_me_left[left_row][left_col] = j - closest_pos
        first_pos_height_left[left_size] = j

import numpy as np

# print(np.array(trees))
# print("down\n", np.array(visible_from_me_down))
# print("right\n", np.array(visible_from_me_right))
# print("up\n", np.array(visible_from_me_up))
# print("left\n", np.array(visible_from_me_left))


def tree_score(row, col):
    return (
        visible_from_me_down[row][col]
        * visible_from_me_right[row][col]
        * visible_from_me_up[row][col]
        * visible_from_me_left[row][col]
    )


best_score = 0
for i in range(SIZE):
    for j in range(SIZE):
        if tree_score(i, j) > best_score:
            best_score = tree_score(i, j)
print(best_score)
