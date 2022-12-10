# part 1
scores = {"X": 1, "Y": 2, "Z": 3}

moves = ["X", "Y", "Z"]
opp_moves = ["A", "B", "C"]


def get_score(move: str, opp_move: str):
    diff = (moves.index(move) - opp_moves.index(opp_move)) % 3
    score = scores.get(move)
    if diff == 0:
        # draw
        score += 3
    elif diff == 1:
        # win
        score += 6
    else:
        # loss
        score += 0
    return score


total_score = 0

with open("input.txt", "r") as f:
    for line in f:
        opp_move, move = line.strip("\n").split(" ")
        total_score += get_score(move, opp_move)

print(total_score)

# part 2
total_score = 0

with open("input.txt", "r") as f:
    for line in f:
        opp_move, outcome = line.strip("\n").split(" ")
        # [lose, draw, win]
        # opp_move - 1 + outcome is our move
        move = moves[(opp_moves.index(opp_move) - 1 + moves.index(outcome)) % 3]
        total_score += get_score(move, opp_move)

print(total_score)
