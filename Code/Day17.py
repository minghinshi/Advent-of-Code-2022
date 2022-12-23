orthogonal_displacements = (0,1), (0,-1), (1,0), (-1,0)

class rock_shape:
    def __init__(self, string: str) -> None:
        self.cells = set()
        lines = string.splitlines()[::-1]
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                if lines[row][col] == "#":
                    self.cells.add((row, col))

class rock:
    def __init__(self, shape, row) -> None:
        self.shape: rock_shape = shape
        self.position = row, 2

    def get_cell_positions(self):
        return {add_vectors(self.position, cell_position) for cell_position in self.shape.cells}

    def has_collision(self, movement, other_cells):
        for cell in self.get_cell_positions():
            new_cell = add_vectors(cell, movement) 
            if not is_within_bounds(new_cell) or new_cell in other_cells:
                return True
        return False

    def move(self, movement):
        self.position = add_vectors(self.position, movement)

class movements:
    def __init__(self, string) -> None:
        self.index = 0
        self.displacements = [self.translate_arrow(char) for char in string]
        self.cycle_length = len(self.displacements)

    def get_displacement(self):
        current_index = self.index
        self.index = (self.index + 1) % self.cycle_length
        return self.displacements[current_index]

    def translate_arrow(self, arrow):
        if arrow == ">":
            return 0, 1
        if arrow == "<":
            return 0, -1
        raise Exception("Error: invalid arrow")

class shape_bag:
    def __init__(self, string) -> None:
        self.index = 0
        self.shapes = [rock_shape(rock_string) for rock_string in string.split("\n\n")]
        self.cycle_length = len(self.shapes)

    def get_shape(self):
        current_index = self.index
        self.index = (self.index + 1) % self.cycle_length
        return self.shapes[current_index]

class snapshot:
    def __init__(self, height, pieces_count, board_shape) -> None:
        self.height = height
        self.pieces = pieces_count
        self.board_shape = board_shape

    def __str__(self) -> str:
        return f"{self.pieces} Pieces: Tower Height = {self.height}"

    def get_first_match(self, others):
        for other in others:
            if other.board_shape == self.board_shape:
                return other

class board:
    def __init__(self, target) -> None:
        self.cells = set()
        self.snapshots: list[snapshot] = []
        self.pieces = 0
        self.target = target
        self.bonus_height = 0
        self.spawn_rock()

    def get_height(self):
        return 0 if len(self.cells) == 0 else max(cell[0] for cell in self.cells) + 1

    def simplify(self):
        height = self.get_height()
        start = height, 0
        unvisited = [start]
        empty_spaces = set()
        exposed_cells = set()
        while len(unvisited) > 0:
            current = unvisited.pop(0)
            for displacement in orthogonal_displacements:
                neighbour = add_vectors(current, displacement)
                if neighbour in self.cells:
                    exposed_cells.add(neighbour)
                elif neighbour not in empty_spaces and is_within_bounds(neighbour) and neighbour[0] <= height:
                    empty_spaces.add(neighbour)
                    unvisited.append(neighbour)
        self.cells = exposed_cells

    def spawn_rock(self):
        self.current_rock = rock(shapes.get_shape(), self.get_height() + 3)

    def calculate_final_height(self):
        while self.pieces != self.target:
            self.step()
        print(f"The height of {self.pieces} pieces is {self.get_height() + self.bonus_height}.")
    
    def step(self):
        if moves.index == 0 and self.bonus_height == 0:
             self.create_snapshot()
        self.move_rock()
    
    def move_rock(self):
        displacement = moves.get_displacement()
        if not self.current_rock.has_collision(displacement, self.cells):
            self.current_rock.move(displacement)
        if self.current_rock.has_collision((-1, 0), self.cells):
            self.stop_rock()
            self.spawn_rock()
        else:
            self.current_rock.move((-1, 0))

    def stop_rock(self):
        self.cells.update(self.current_rock.get_cell_positions())
        self.pieces += 1
        if self.pieces % 10 == 0:
            self.simplify()

    def create_snapshot(self):
        new_snapshot = snapshot(self.get_height(), self.pieces, self.get_board_shape())
        print(new_snapshot)
        prev_snapshot = new_snapshot.get_first_match(self.snapshots)
        if prev_snapshot is None:
            self.snapshots.append(new_snapshot)
        else:
            self.accelerate_simulation(new_snapshot, prev_snapshot)

    def accelerate_simulation(self, new_snapshot: snapshot, prev_snapshot: snapshot):
        print(f"Matching snapshot found! Previous snapshot had {prev_snapshot.pieces} pieces.")
        pieces_gain = new_snapshot.pieces - prev_snapshot.pieces
        height_gain = new_snapshot.height - prev_snapshot.height
        cycles = (self.target - self.pieces) // pieces_gain
        self.pieces += pieces_gain * cycles
        self.bonus_height = height_gain * cycles
        print(f"Skipped ahead to {self.pieces} pieces and increased height by {self.bonus_height}.")

    def get_board_shape(self):
        self.simplify()
        height = self.get_height()
        cells = set.union(self.cells, self.current_rock.get_cell_positions())
        return set((cell[0]-height, cell[1]) for cell in cells)

    def print(self):
        for row in range(self.get_height() + 4)[::-1]:
            print("|", end="")
            for col in range(7):
                if (row, col) in self.cells:
                    cell = "#"
                else:
                    cell = "."
                print(cell, end="")
            print("|")
        print("+-------+")
        
with open("Inputs/Rocks.txt") as file:
    shapes = shape_bag(file.read()) 
with open("Inputs/Day17.txt") as file:
    moves = movements(file.read().strip())

def add_vectors(*vectors):
    return tuple(map(sum, zip(*vectors)))

def is_within_bounds(cell):
    return cell[0] >= 0 and cell[1] >= 0 and cell[1] < 7

board(1000000000000).calculate_final_height()