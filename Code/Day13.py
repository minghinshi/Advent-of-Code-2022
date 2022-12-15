from functools import cmp_to_key, reduce
from operator import mul

def compare_lists(left: list, right: list):
    for i in range(min(len(left), len(right))):
        result = compare(left[i], right[i])
        if result != 0: return result
    return len(left) - len(right)

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    left_list = left if isinstance(left, list) else [left]
    right_list = right if isinstance(right, list) else [right]
    return compare_lists(left_list, right_list)

with open("Inputs/Day13.txt") as file:
    lists = [eval(line) for line in file.read().split() if not line.isspace()]

print(sum(i+1 for i in range(len(lists) // 2) if compare(lists[2*i], lists[2*i+1]) < 0))

targets = [[2]], [[6]]
lists.extend(targets)
lists.sort(key = cmp_to_key(compare))
print(reduce(mul, map(lambda x: lists.index(x)+1, targets)))