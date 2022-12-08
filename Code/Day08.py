def get_grid():
    with open("Inputs/Day08.txt") as file:
        return [list(map(int, line)) for line in file.read().splitlines()]

def product(list):
    result = 1
    for number in list:
        result *= number
    return result

def first_is_highest(list):
    return len(list) <= 1 or list[0] > max(list[1:])

def count_visible_trees(list):
    count = 0
    for cell in list[1:]:
        count += 1
        if cell >= list[0]: 
            break
    return count

def iterate_grid(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            yield r, c

def get_lines_of_sight(grid, row, column):
    height, width = len(grid), len(grid[0])
    up = [grid[r][column] for r in range(row, -1, -1)]
    down = [grid[r][column] for r in range(row, height)]
    left = [grid[row][c] for c in range(column, -1, -1)]
    right = [grid[row][c] for c in range(column, width)]
    return up, down, left, right

def is_visible(lines):
    return any(map(first_is_highest, lines))

def get_score(lines):
    return product(map(count_visible_trees, lines))

def main():
    grid = get_grid()
    lines_of_sight = [get_lines_of_sight(grid, r, c) for r, c in iterate_grid(grid)]
    print(sum(map(is_visible, lines_of_sight)), max(map(get_score, lines_of_sight)))

main()