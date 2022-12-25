choices = (0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)

def add_vectors(*vectors):
    return tuple(map(sum, zip(*vectors)))

class blizzard:
    def __init__(self, position, direction) -> None:
        self.displacement = get_displacement(direction)
        self.position = position

    def move(self, board):
        self.position = add_vectors(self.position, self.displacement)
        if not board.is_within_bounds(self.position):
            self.wrap_around(board.height, board.width)

    def wrap_around(self, height, width):
        self.position = self.position[0] % height, self.position[1] % width

class board:
    def __init__(self, string: str) -> None:
        lines = string.splitlines()
        self.height = len(lines) - 2
        self.width = len(lines[0]) - 2
        self.parse_blizzards(lines)
        self.possible_positions = {self.get_start()}

    def parse_blizzards(self, lines):
        self.blizzards: list[blizzard] = []
        for row in range(self.height):
            for col in range(self.width):
                char = lines[row+1][col+1]
                if char != ".":
                    self.blizzards.append(blizzard((row, col), char))

    def is_within_bounds(self, cell):
        if cell == self.get_start() or cell == self.get_end():
            return True
        return 0 <= cell[0] < self.height and 0 <= cell[1] < self.width

    def move_blizzards(self):
        for blizzard in self.blizzards:
            blizzard.move(self)

    def get_blizzard_positions(self):
        return {blizzard.position for blizzard in self.blizzards}

    def move_character(self):
        blizzard_positions = self.get_blizzard_positions()
        new_positions = set()
        for position in self.possible_positions:
            for choice in choices:
                new_position = add_vectors(position, choice)
                if new_position not in blizzard_positions and self.is_within_bounds(new_position):
                    new_positions.add(new_position)
        self.possible_positions = new_positions

    def walk(self, target):
        moves = 0
        while target not in self.possible_positions:
            self.move_blizzards()
            self.move_character()
            moves += 1
        self.possible_positions = {target}
        return moves

    def get_start(self):
        return -1, 0

    def get_end(self):
        return self.height, self.width - 1

def get_displacement(direction):
    if direction == "v":
        return 1, 0
    if direction == "^":
        return -1, 0
    if direction == ">":
        return 0, 1
    if direction == "<":
        return 0, -1

with open("Inputs/Day24.txt") as file:
    board_object = board(file.read())
first = board_object.walk(board_object.get_end())
second = board_object.walk(board_object.get_start())
third = board_object.walk(board_object.get_end())
print(first)
print(first + second + third)