def parse_digit(digit):
    if digit == "=":
        return -2
    if digit == "-":
        return -1
    return int(digit)

def to_array(line):
    return [parse_digit(digit) for digit in line][::-1]

def get_value(array):
    return sum(5 ** i * array[i] for i in range(len(array)))

def to_base_five(number):
    array = []
    while number != 0:
        number, remainder = divmod(number, 5)
        array.append(remainder)
    return array

def shift_digits(array):
    for i in range(len(array)):
        if array[i] > 2:
            array[i] -= 5
            if i+1 == len(array):
                array.append(1)
            else:
                array[i+1] += 1
    return array

def to_string(digit):
    if digit == -2:
        return "="
    if digit == -1:
        return "-"
    return str(digit)

with open("Inputs/Day25.txt") as file:
    lines = file.read().splitlines()
total = sum(get_value(to_array(line)) for line in lines)
print("".join(to_string(digit) for digit in shift_digits(to_base_five(total)))[::-1])