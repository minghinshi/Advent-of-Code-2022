class monkey:
    def __init__(self, starting_items, operation, modulus, targets) -> None:
        self.items: list[dict[int, int]] = starting_items
        self.operation: function = operation
        self.modulus: int = modulus
        self.targets: list[int] = targets
        self.inspections = 0

    def send_all_items(self):
        while len(self.items) != 0:
            self.send_item()
            self.inspections += 1
    
    def send_item(self):
        item = operate_on_table(self.items.pop(0), self.operation)
        target = self.targets[(item[self.modulus] == 0)]
        monkeys[target].receive_item(item)
        
    def receive_item(self, item):
        self.items.append(item)

def parse_operation(string: str):
    strings = string.split()
    if strings[4] == "*":
        if strings[5] == "old":
            return lambda x: x ** 2
        else:
            return lambda x: x * int(strings[5])
    elif strings[4] == "+":
        return lambda x: x + int(strings[5])
    print("Error: Cannot parse operation.")

def parse_starting_items(string: str):
    numbers = string.removeprefix("  Starting items: ").split(", ")
    return [get_residue_table(int(number)) for number in numbers]

def get_moduli(string: str):
    prefix = "  Test: divisible by "
    return [int(line.removeprefix(prefix)) for line in string.splitlines() if line.startswith(prefix)]

def get_residue_table(number: int):
    return {modulus: number % modulus for modulus in moduli}

def operate_on_table(residue_table: dict[int, int], operation):
    for modulus, residue in residue_table.items():
        residue_table[modulus] = operation(residue) % modulus
    return residue_table

def parse_monkey(string: str):
    lines = string.splitlines()
    starting_items = parse_starting_items(lines[1])
    operation = parse_operation(lines[2])
    modulus = int(lines[3].split()[-1])
    targets = [int(line.split()[-1]) for line in (lines[5], lines[4])]
    return monkey(starting_items, operation, modulus, targets)

with open("Inputs/Day11.txt") as file:
    content = file.read()
    moduli = get_moduli(content)
    monkeys = list(map(parse_monkey, content.split("\n\n")))

for i in range(10000):
    for monkey in monkeys:
        monkey.send_all_items()

monkeys.sort(key = lambda monkey: monkey.inspections, reverse = True)
print(monkeys[0].inspections * monkeys[1].inspections)