def get_same_item(*strings):
    sets = map(set, strings)
    return list(set.intersection(*sets))[0]

def get_priority(letter):
    if "A" <= letter <= "Z":
        return ord(letter) - 38
    elif "a" <= letter <= "z":
        return ord(letter) - 96

with open("Inputs/Day03.txt") as file:
    inputs = file.read().splitlines()

total = 0
for line in inputs:
    mid = len(line) // 2
    item = get_same_item(line[:mid], line[mid:])
    total += get_priority(item)
print(total)

total = 0
for i in range(0, len(inputs), 3):
    item = get_same_item(*inputs[i:i+3])
    total += get_priority(item)
print(total)