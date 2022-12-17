class player:
    def __init__(self, location, time_left) -> None:
        self.location = location
        self.time_left = time_left

class node:
    def __init__(self, locations, opened_valves, time_lefts, pressure) -> None:
        self.locations: list[str] = locations
        self.time_lefts: list[int] = time_lefts
        self.pressure: int = pressure
        self.opened_valves: set[str] = opened_valves

    def get_flow_rate(self):
        return flow_rates[self.location]

    def can_open_valve(self, valve, player):
        return valve not in self.opened_valves and compressed_graph[self.locations[player]][valve] < self.time_left

    def open_valve(self, valve, player):
        new_locations = self.locations.copy()
        new_locations[player] = valve
        new_time_left = self.time_lefts.copy()
        new_time_left[player] -= compressed_graph[self.locations[player]][valve]
        new_pressure = self.pressure + flow_rates[valve] * new_time_left[player]
        new_opened_valves = self.opened_valves.copy()
        new_opened_valves.add(valve)
        return node(new_locations, new_opened_valves, new_time_left, new_pressure)

    def get_neighbours(self):
        return {self.open_valve(valve) for valve in filter(self.can_open_valve, valves)}

    def get_key(self):
        return self.location, tuple(self.opened_valves)

    def print(self):
        print(self.location, self.opened_valves, self.time_left, self.pressure)

def sign(x):
    return -1 if x < 0 else 0 if x == 0 else 1

def parse_line(strings: str):
    name = strings[1]
    flow_rates[name] = int(strings[4][5:-1])
    graph[name] = [string.removesuffix(",") for string in strings[9:]]

def get_max_pressure(root: node):
    nodes = {root.get_key(): [root]}
    unvisited = [root]
    while len(unvisited) != 0:
        current_node = unvisited.pop(0)
        current_node.print()
        for node in current_node.get_neighbours():
            add_to_queue = True
            for other in nodes.setdefault(node.get_key(), []):
                if not node.any_better_than(other):
                    add_to_queue = False
                if node.both_better_than(other):                   
                    nodes[node.get_key()].remove(other)
                    if other in unvisited:
                        unvisited.remove(other)
            if add_to_queue:
                nodes[node.get_key()].append(node)
                unvisited.append(node)
    return max(max(node.pressure for node in list) for list in nodes.values())

def get_max_pressure_greedy(root: node):
    current = root
    while True:
        neighbours = current.get_neighbours()
        if len(neighbours) == 0:
            return current.pressure
        current = sorted(neighbours, key=lambda x: x.pressure)[-1]
        
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

flow_rates = {}
graph = {}

with open("Inputs/Day16.txt") as file:
    for line in file.read().splitlines():
        parse_line(line.split())

valves = get_target_valves()
compressed_graph = compress_graph()

print(get_max_pressure(node("AA", set(), 30, 0)))