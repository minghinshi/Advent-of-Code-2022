def shuffle(number_list, count):
    list_size = len(number_list)
    indices = list(range(list_size))
    for _ in range(count):
        for i in range(list_size):
            position = indices.index(i)
            del indices[position]
            indices.insert((position + number_list[i]) % (list_size - 1), i)
    return indices

def apply_ordering(number_list, ordering):
    return [number_list[i] for i in ordering]

def calculate_coordinates(number_list, shuffle_count):
    new_indices = shuffle(number_list, shuffle_count)
    new_list = apply_ordering(number_list, new_indices)
    zero_position = new_list.index(0)
    print(sum(new_list[(zero_position + i) % len(new_list)] for i in (1000, 2000, 3000)))

def main():
    with open("Inputs/Day20.txt") as file:
        number_list = [int(line) for line in file]
    calculate_coordinates(number_list, 1)
    calculate_coordinates([number * 811589153 for number in number_list], 10)

main()