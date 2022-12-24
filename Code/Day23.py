eight_displacements = (0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)

def add_vectors(*vectors):
    return tuple(map(sum, zip(*vectors)))

def get_bounds(points):
    return tuple(map(min, zip(*points))), tuple(map(max, zip(*points)))

def get_board_size(board):
    min_bound, max_bound = get_bounds(board)
    return (max_bound[0] - min_bound[0] + 1) * (max_bound[1] - min_bound[1] + 1)

class movement:
    def __init__(self, displacement: tuple[int], checked_cells: set[tuple[int]]) -> None:
        self.displacement = displacement
        self.checked_cells = checked_cells

    def is_blocked(self, cell, board):
        for checked_cell in self.checked_cells:
            if add_vectors(cell, checked_cell) in board:
                return True
        return False

class movement_bag:
    def __init__(self) -> None:
        self.moves: list[movement] = []
        self.moves.append(movement((-1, 0), {(-1, -1), (-1, 0), (-1, 1)}))
        self.moves.append(movement((1, 0), {(1, -1), (1, 0), (1, 1)}))
        self.moves.append(movement((0, -1), {(-1, -1), (0, -1), (1, -1)}))
        self.moves.append(movement((0, 1), {(-1, 1), (0, 1), (1, 1)}))

    def get_destination(self, cell, board):
        if count_neighbours(cell, board) == 0:
            return cell
        for move in self.moves:
            if not move.is_blocked(cell, board):
                return add_vectors(cell, move.displacement)
        return cell

    def cycle_bag(self):
        first_move = self.moves.pop(0)
        self.moves.append(first_move)

    def print(self):
        for move in self.moves:
            print(move.displacement)

def parse_board(lines):
    board = set()
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == "#":
                board.add((row, col))
    return board

def count_neighbours(cell, board):
    return sum(add_vectors(cell, displacement) in board for displacement in eight_displacements)

def get_cell_destinations(board):
    destinations = {cell: moves.get_destination(cell, board) for cell in board}
    remove_repeated_destinations(destinations)
    return destinations

def remove_repeated_destinations(destinations: dict):
    repeated = get_repeated_items(list(destinations.values()))
    for cell, destination in destinations.items():
        if destination in repeated:
            destinations[cell] = cell

def get_repeated_items(list: list):
    temp = list.copy()
    for item in set(list):
        temp.remove(item)
    return set(temp)

def step(board):
    destinations = get_cell_destinations(board)
    moves.cycle_bag()
    return {destinations[cell] for cell in board}

def simulate(board):
    moves = 0
    previous_board = None
    while previous_board != board:
        moves += 1
        print(f"Simulating round {moves}...")
        previous_board = board
        board = step(board)
        if moves == 10:
            print(f"Empty spaces = {get_board_size(board) - len(board)}")
    print(f"Simulation ended after {moves} moves.")

def print_board(board):
    string = ""
    min_bound, max_bound = get_bounds(board)
    for row in range(min_bound[0], max_bound[0]+1):
        for col in range(min_bound[1], max_bound[1]+1):
            string += "#" if (row, col) in board else "."
        string += "\n"
    print(string)

moves = movement_bag()
with open("Inputs/Day23.txt") as file:
    board = parse_board(file.read().splitlines())
simulate(board)