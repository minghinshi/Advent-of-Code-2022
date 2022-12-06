def are_unique(string: str):
    return len(set(string)) == len(string)

def get_marker_index(string: str, count: int):
    for i in range(len(string)):
        if are_unique(string[i:i+count]):
            return i+count

def main():
    with open("Inputs/Day06.txt") as file:
        input = file.read()
    print(get_marker_index(input, 4))
    print(get_marker_index(input, 14))

main()