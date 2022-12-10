def parse_line(line):
    strings = line.split()
    if strings[0] == "noop":
        return 0, 1
    elif strings[0] == "addx":
        return int(strings[1]), 2

def get_input():
    with open("Inputs/Day10.txt") as file:
        return file.read().splitlines()

def get_pixel(register, position):
    return "#" if abs(register - position) <= 1 else "."

register = 1
cycles = 0
checksum = 0
display = ""

for change, cycle_count in map(parse_line, get_input()):
    for _ in range(cycle_count):
        display += get_pixel(register, cycles % 40)
        cycles += 1
        if cycles % 40 == 20:
            checksum += cycles * register
    register += change

print(checksum)
for i in range(0, 240, 40):
    print(display[i:i+40])