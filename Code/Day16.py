import copy

class player:
    def __init__(self) -> None:
        self.location = "AA"
        self.time_to_spend = 0

    def move_to_valve(self, valve):
        self.time_to_spend -= compressed_graph[self.location][valve]
        self.location = valve

    def get_choices(self, opened_valves):
        choices = set()
        for valve in get_target_valves():
            if valve not in opened_valves and compressed_graph[self.location][valve] <= self.time_to_spend:
                choices.add(valve)
        return choices

    def __str__(self) -> str:
        return f"Player at {self.location} with {self.time_to_spend} minutes to spend."

class node:
    def __init__(self, player_count, moves_allowed) -> None:
        self.players = [player() for _ in range(player_count)]
        self.moves_left = moves_allowed
        self.opened_valves = set()
        self.pressure = 0
        self.turn = 0

    def open_valve(self, valve):
        self.get_current_player().move_to_valve(valve)
        self.opened_valves.add(valve)
        self.pressure += (self.moves_left - 1) * flow_rates[valve]

    def elapse_turn(self):
        self.turn += 1
        if self.turn == len(self.players):
            self.turn = 0
            self.moves_left -= 1

    def get_current_player(self) -> player:
        return self.players[self.turn]

    def get_children(self):
        children = set()

        # First, the player on this round gets 1 time to spend:
        player = self.get_current_player()
        player.time_to_spend += 1

        # Then, the player thinks about where to spend their time:
        for choice in player.get_choices(self.opened_valves):
            child = copy.deepcopy(self)
            child.open_valve(choice)
            child.elapse_turn()
            children.add(child)

        # The player can also choose to do nothing
        child = copy.deepcopy(self)
        child.elapse_turn()
        children.add(child)
      
        return children

    def __str__(self) -> str:
        string = ""
        for player in self.players:
            string += f"{player}\n"
        string += f"Opened valves: {self.opened_valves}. {self.pressure} pressure released.\n"
        string += f"It is currently Player {self.turn+1}'s turn. {self.moves_left} minutes left.\n"
        return string

def parse_line(strings: str):
    name = strings[1]
    flow_rates[name] = int(strings[4][5:-1])
    graph[name] = [string.removesuffix(",") for string in strings[9:]]

        
def get_shortest_paths(root, targets):
    costs = {root: 0}
    unvisited = [root]
    while len(unvisited) != 0:
        valve = unvisited.pop(0)
        for neighbour in graph[valve]:
            if neighbour not in costs:
                costs[neighbour] = costs[valve] + 1
                unvisited.append(neighbour)
    return {target: costs[target]+1 for target in targets if target != root}

def get_target_valves():
    return {valve for valve in flow_rates if flow_rates[valve] > 0}

def compress_graph():
    compressed_graph = {}
    for target in valves:
        compressed_graph[target] = get_shortest_paths(target, valves)
    compressed_graph["AA"] = get_shortest_paths("AA", valves)
    return compressed_graph

def get_highest_pressure(player_count, moves_allowed):
    nodes = [node(player_count, moves_allowed)]
    for i in range(player_count * moves_allowed):
        print(f"Iterations = {i+1}, Nodes = {len(nodes)}")
        children: list[node] = []
        for current in nodes:
            children.extend(current.get_children())
        children.sort(key=lambda x: x.pressure)
        children.reverse()
        nodes = children[:1000]
    return max(map(lambda x: x.pressure, nodes))
            
flow_rates = {}
graph = {}

with open("Inputs/Day16.txt") as file:
    for line in file.read().splitlines():
        parse_line(line.split())

valves = get_target_valves()
compressed_graph = compress_graph()
print(get_highest_pressure(1, 30))
print(get_highest_pressure(2, 26))