def parse_stacks(stacks_input: str):
    lines = stacks_input.splitlines()
    input_length = len(lines.pop())
    lines.reverse()
    return [[line[i] for line in lines if line[i] != " "] for i in range(1, input_length, 4)]
    
def parse_move(move: str):
    commands = move.split()
    return int(commands[1]), int(commands[3])-1, int(commands[5])-1

def parse_moves(move_input: str):
    return map(parse_move, move_input.splitlines())

def perform_move_1(count: int, start: list[str], end: list[str]):
    for _ in range(count):
        end.append(start.pop())

def perform_move_2(count: int, start: list[str], end: list[str]):
    end.extend(start[-count:])
    del start[-count:]

def perform_moves(stacks: list[list[str]], moves: list[tuple[int]], move_method):
    for count, start_index, end_index in moves:
        move_method(count, stacks[start_index], stacks[end_index])

def get_answer(stacks: list[list[str]]):
    return "".join(stack[-1] for stack in stacks)

def solve_puzzle(move_method):
    with open("Inputs/Day05.txt") as file:
        stacks_input, moves_input = file.read().split("\n\n")
    stacks = parse_stacks(stacks_input)
    moves = parse_moves(moves_input)
    perform_moves(stacks, moves, move_method)
    print(get_answer(stacks))

solve_puzzle(perform_move_1)
solve_puzzle(perform_move_2)