with open("Inputs/Day01.txt") as file:
    inputs = file.read()

calories = [sum(map(int, group.split("\n"))) for group in inputs.split("\n\n")]

def get_sum_of_highest(count):
    return sum(sorted(calories, reverse=True)[:count])

print(get_sum_of_highest(1))
print(get_sum_of_highest(3))