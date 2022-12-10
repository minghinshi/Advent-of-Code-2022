orthogonals = {(0,1), (0,-1), (1,0), (-1,0)}
diagonals = {(1,1), (1,-1), (-1,1), (-1,-1)}

def is_adjacent(point1, point2):
    return abs(point1[0] - point2[0]) < 2 and abs(point1[1] - point2[1]) < 2

def same_row_or_col(point1, point2):
    return point1[0] == point2[0] or point1[1] == point2[1]

def get_change(direction):
    if direction == "U":
        return 0, 1
    elif direction == "D":
        return 0, -1  
    elif direction == "L":
        return -1, 0
    elif direction == "R":
        return 1, 0 

def parse_movement(line):
    strings = line.split()
    return get_change(strings[0]), int(strings[1])  

def get_movements():
    with open("Inputs/Day09.txt") as file:
        return map(parse_movement, file.read().splitlines())

def add_vectors(point, change):
    return (point[0] + change[0], point[1] + change[1])

def update_tail(head, tail):
    moves = orthogonals if same_row_or_col(head, tail) else diagonals
    for point in [add_vectors(tail, move) for move in moves]:
        if is_adjacent(head, point):
            return point

def update_rope(rope, index):
    if index + 1 != len(rope) and not is_adjacent(rope[index], rope[index + 1]):
        rope[index + 1] = update_tail(rope[index], rope[index + 1])
        update_rope(rope, index + 1)

def main():
    rope = [(0,0) for _ in range(10)]
    second_visited = {(0,0)}
    last_visited = {(0,0)}
    for change, magnitude in get_movements():
        for _ in range(magnitude):
            rope[0] = add_vectors(rope[0], change)
            update_rope(rope, 0)
            second_visited.add(rope[1])
            last_visited.add(rope[-1])
    print(len(second_visited), len(last_visited))

main()