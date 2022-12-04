with open("Inputs/Day04.txt") as file:
    inputs = file.read().splitlines()

def contains(tuple1, tuple2):
    return tuple1[0] <= tuple2[0] and tuple1[1] >= tuple2[1]

def any_contains(tuple1, tuple2):
    return contains(tuple1, tuple2) or contains(tuple2, tuple1)

def has_overlap(tuple1, tuple2):
    if tuple1[0] > tuple2[0]:
        tuple1, tuple2 = tuple2, tuple1
    return tuple1[1] >= tuple2[0]

def parse_time_range(string):
    return tuple(map(int, string.split("-")))

contain_count = 0
overlap_count = 0
for line in inputs:
    tuple1, tuple2 = map(parse_time_range, line.split(","))
    contain_count += any_contains(tuple1, tuple2)
    overlap_count += has_overlap(tuple1, tuple2)
print(contain_count, overlap_count)