class blueprint:
    def __init__(self, line: str) -> None:
        strings = line.split()
        self.id = int(strings[1].removesuffix(":"))
        self.robot_costs: list[dict] = []
        self.robot_costs.append({0: int(strings[6])})
        self.robot_costs.append({0: int(strings[12])})
        self.robot_costs.append({0: int(strings[18]), 1: int(strings[21])})
        self.robot_costs.append({0: int(strings[27]), 2: int(strings[30])})

    def can_build(self, items, robot_type):
        for item_type, cost in self.robot_costs[robot_type].items():
            if items[item_type] < cost:
                return False
        return True

    def can_build_all(self, items):
        return all(self.can_build(items, i) for i in range(4))

    def spend_items(self, items, robot_type):
        for item_type, cost in self.robot_costs[robot_type].items():
            items[item_type] -= cost

    def max_ore_cost(self):
        return max(cost[0] for cost in self.robot_costs)

    def max_ore_cost_except_ore_robot(self):
        return max(cost[0] for cost in self.robot_costs[1:])

class simulation:
    def __init__(self, bp, robots, items, time_left, robot_to_build) -> None:
        self.bp: blueprint = bp
        self.robots: list[int] = robots
        self.items: list[int] = items
        self.time_left = time_left
        self.robot_to_build = robot_to_build
        self.gather_items()
        self.build_robot()
        self.production_forecast = self.forecast_production()

    def gather_items(self):
        for i in range(4):
            self.items[i] += self.robots[i]
        self.time_left -= 1

    def build_robot(self):
        if self.robot_to_build is not None:
            self.bp.spend_items(self.items, self.robot_to_build)
            self.robots[self.robot_to_build] += 1

    def forecast_production(self):
        return [self.items[i] + self.robots[i] * self.time_left for i in range(4)]

    def get_next_steps_greedy(self):
        if self.time_left == 0:
            return []
        # If there is enough obsidian, spend the obsidian first
        if self.bp.can_build(self.items, 3):
            return [simulation(self.bp, self.robots.copy(), self.items.copy(), self.time_left, 3)]
        # If there is enough clay, spend the clay first
        if self.bp.can_build(self.items, 2):
            return [simulation(self.bp, self.robots.copy(), self.items.copy(), self.time_left, 2)]
        next_purchases = set()
        # If there's enough robots to sustain 1 robot / min, there's no point in building more
        if self.bp.can_build(self.items, 0) and self.robots[0] < self.bp.max_ore_cost_except_ore_robot():
            next_purchases.add(0)
        if self.bp.can_build(self.items, 1):
            next_purchases.add(1)
        # Sometimes you need to save for obsidian and geode robots
        if self.items[0] < self.bp.max_ore_cost():
            next_purchases.add(None)
        return [simulation(self.bp, self.robots.copy(), self.items.copy(), self.time_left, purchase) for purchase in next_purchases]

    def get_next_steps(self):
        if self.time_left == 0:
            return []
        next_purchases = set()
        if not self.bp.can_build_all(self.items):
            next_purchases.add(None)
        if self.bp.can_build(self.items, 3):
            next_purchases.add(3)
        if self.bp.can_build(self.items, 2) and self.production_forecast[2] < self.bp.robot_costs[3][2] * self.time_left:
            next_purchases.add(2)
        if self.bp.can_build(self.items, 1) and self.production_forecast[1] < self.bp.robot_costs[2][1] * self.time_left:
            next_purchases.add(1)
        if self.bp.can_build(self.items, 0) and self.production_forecast[0] < self.bp.max_ore_cost_except_ore_robot() * self.time_left:
            next_purchases.add(0)
        return [simulation(self.bp, self.robots.copy(), self.items.copy(), self.time_left, purchase) for purchase in next_purchases]

def search(root: simulation):
    nodes = [root]
    unvisited = [root]
    while len(unvisited) != 0:
        current = unvisited.pop(0)
        for neighbour in current.get_next_steps_greedy():
            nodes.append(neighbour)
            unvisited.append(neighbour)
    return nodes

def iterate(root: simulation, iterations):
    nodes = [root]
    for _ in range(iterations):
        children: list[simulation] = []
        for node in nodes:
            children.extend(node.get_next_steps())
        children.sort(key=lambda x: x.production_forecast[::-1])
        children.reverse()
        nodes = children[:10000]
    return nodes

def get_max_geodes(simulations: list[simulation]):
    return max(simulation.items[3] for simulation in simulations)

def solve_part_1(blueprints):
    total = 0
    for bp in blueprints:
        sim = simulation(bp, [1, 0, 0, 0], [0, 0, 0, 0], 24, None)
        max_geodes = get_max_geodes(iterate(sim, 23))
        print(f"Blueprint {bp.id}: {max_geodes}")
        total += bp.id * max_geodes
    print(total)

def solve_part_2(blueprints):
    product = 1
    for bp in blueprints:
        sim = simulation(bp, [1, 0, 0, 0], [0, 0, 0, 0], 32, None)
        max_geodes = get_max_geodes(iterate(sim, 31))
        print(f"Blueprint {bp.id}: {max_geodes}")
        product *= max_geodes
    print(product)

def main():
    with open("Inputs/Day19.txt") as file:
        blueprints = [blueprint(line) for line in file]
    solve_part_1(blueprints)
    solve_part_2(blueprints[:3])

main()