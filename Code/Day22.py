unit_vectors = (0, 1), (1, 0), (0, -1), (-1, 0)

def add_vectors(*vectors):
    return tuple(map(sum, zip(*vectors)))

def rotate_cw(board: list[list]):
    board_size = len(board)
    return [[board[board_size-col-1][row] for col in range(board_size)] for row in range(board_size)]

def rotate_180(board: list[list]):
    return [row[::-1] for row in board][::-1]

def rotate_ccw(board: list[list]):
    board_size = len(board)
    return [[board[col][board_size-row-1] for col in range(board_size)] for row in range(board_size)]

def get_dimensions(board: list[list]):
    return len(board), len(board[0])

def parse_board(string: str):
    lines = string.splitlines()
    board_width = max(len(line) for line in lines)
    for i in range(len(lines)):
        lines[i] = list(f"{lines[i]:<{board_width}}")
    return lines

def get_net_size(board: list[list]):
    return (5, 2 if len(board) * 2 == len(board[0]) * 5 else 4, 3)

def parse_net(string: str):
    board = parse_board(string)
    if len(board) < len(board[0]):
        board = rotate_cw(board)
    net_height, net_width = get_net_size(board)
    square_size = len(board) // net_height
    # TODO: Continue this part

def parse_commands(string: str):
    commands = []
    temp = ""
    for char in string:
        if char == "L" or char == "R":
            if len(temp) > 0:
                commands.append(int(temp))
                temp = ""
            commands.append(char)
        else:
            temp += char
    if len(temp) > 0:
        commands.append(int(temp))
    return commands

def parse_input(string: str):
    strings = string.split("\n\n")
    return parse_board(strings[0]), parse_commands(strings[1])

def get_first_cell_pos(line: str):
    for i in range(len(line)):
        if not line[i].isspace():
            return i

def is_out_of_bounds(board, row, col):
    return row >= len(board) or col >= len(board[row]) or board[row][col] == " "  

def get_line(board, row, col, direction) -> str:
    if direction == 0:
        return board[row]
    if direction == 1:
        return "".join(board[r][col] for r in range(len(board)))
    return get_line(board, row, col, direction-2)[::-1]

def get_edge(board, row, col, direction):
    line_of_sight = get_line(board, row, col, direction)
    first_cell_pos = get_first_cell_pos(line_of_sight)
    if direction == 0:
        return row, first_cell_pos
    if direction == 1:
        return first_cell_pos, col
    if direction == 2:
        return row, len(board[row]) - first_cell_pos - 1
    if direction == 3:
        return len(board) - first_cell_pos - 1, col

def get_next_step(board, position, direction):
    unit_vector = unit_vectors[direction]
    new_position = add_vectors(position, unit_vector)
    if is_out_of_bounds(board, *new_position):
        new_position = get_edge(board, *position, direction)
    return new_position

def move(board, position, distance, direction):
    for _ in range(distance):
        new_position = get_next_step(board, position, direction)
        row, col = new_position
        if board[row][col] == "#":
            return position
        position = new_position
    return position

def rotate(direction, rotate_direction):
    if rotate_direction == "R":
        return (direction + 1) % 4
    if rotate_direction == "L":
        return (direction - 1) % 4 

def walk_the_board(board, commands):
    position = 0, get_first_cell_pos(board[0])
    direction = 0
    for command in commands:
        if command == "L" or command == "R":
            direction = rotate(direction, command)
        else:
            position = move(board, position, command, direction)
    return position, direction

def main():
    with open("Inputs/Day22.txt") as file:
        board, commands = parse_input(file.read())
    position, direction = walk_the_board(board, commands)
    print(1000 * (position[0] + 1) + 4 * (position[1] + 1) + direction)
 
main()