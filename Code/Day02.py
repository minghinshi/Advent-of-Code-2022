mapping = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}

def result(player1, player2):
    return (player2 - player1 + 1) % 3

def score(player1, player2):
    return result(player1, player2) * 3 + player2

def get_move(player1, instruction):
    return (player1 + instruction) % 3 + 1

def translate(letter):
    return mapping[letter]

with open("Inputs/Day02.txt") as file:
    inputs = file.read()

first_total = 0
second_total = 0
for line in inputs.split("\n"):
    key1, key2 = map(translate, line.split())
    first_total += score(key1, key2)
    move = get_move(key1, key2)
    second_total += score(key1, move)
print(first_total, second_total)