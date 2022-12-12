def get_altitude(letter):
    if letter == "S":
        return 0
    elif letter == "E":
        return 25
    else:
        return ord(letter) - 97

def get_adjacent_coordinates(row, col):
    return (row+1, col), (row-1, col), (row, col-1), (row, col+1)

def get_edges(nodes, coord):
    return [adjacent for adjacent in get_adjacent_coordinates(*coord) if adjacent in nodes and nodes[adjacent] - nodes[coord] <= 1]

def parse_input(string: str):
    nodes = {}
    lines = string.splitlines()
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            letter = lines[row][col]
            nodes[row, col] = get_altitude(letter)
            if letter == "S":
                start = row, col
            elif letter == "E":
                end = row, col
    return nodes, start, end

def construct_graph(nodes: dict):
    return {coord: get_edges(nodes, coord) for coord in nodes}

def bfs(graph, start):
    costs = {start: 0}
    queue = [start]
    while len(queue) != 0:
        node = queue.pop(0)
        for next in graph[node]:
            if next not in costs:
                costs[next] = costs[node] + 1
                queue.append(next)
    return costs
            
with open("Inputs/Day12.txt") as file:
    nodes, start, end = parse_input(file.read())
    graph = construct_graph(nodes)

costs_from_low_point = {}
for coord in filter(lambda x: nodes[x] == 0, nodes):
    costs = bfs(graph, coord)
    if end in costs:
        costs_from_low_point[coord] = costs[end]
print(costs_from_low_point[start], min(costs_from_low_point.values()))