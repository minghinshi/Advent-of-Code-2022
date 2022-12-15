def parse_coordinate(string):
    return tuple(map(int, string.split(",")))

def parse_line(string):
    corners = list(map(parse_coordinate, string.split("->")))
    points = set(corners)
    for i in range(1, len(corners)):
        points = points.union(get_wall(*corners[i-1], *corners[i]))
    return points

def get_wall(x1, y1, x2, y2):
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        return [(x1, y) for y in range(y1+1, y2)]
    elif y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        return [(x, y1) for x in range(x1+1, x2)]

def get_floor(obstacles):
    return max(obstacle[1] for obstacle in obstacles) + 2

def is_blocked(x, y):
    return y == floor or (x, y) in obstacles

def get_next_step(x, y):
    if not is_blocked(x, y+1):
        return x, y+1
    elif not is_blocked(x-1, y+1):
        return x-1, y+1
    elif not is_blocked(x+1, y+1):
        return x+1, y+1
    return x, y

def run_simulation():
    current = 500, 0
    while True:
        next_step = get_next_step(*current)
        if next_step == current:
            return current
        current = next_step

def get_sand_count():
    return len(obstacles) - rock_count

with open("Inputs/Day14.txt") as file:
    lines = file.read().splitlines()

obstacles = set.union(*map(parse_line, lines))
floor = get_floor(obstacles)
rock_count = len(obstacles)
reached_floor = False

while True:
    sand = run_simulation()
    if not reached_floor and sand[1]+1 == floor:
        print(get_sand_count())
        reached_floor = True
    obstacles.add(sand)
    if sand == (500, 0):
        print(get_sand_count())
        break