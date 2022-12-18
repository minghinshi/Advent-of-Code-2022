offsets = (1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)

def add_vectors(*vectors):
    return tuple(map(sum, zip(*vectors)))

def get_neighbours(point):
    return [add_vectors(point, offset) for offset in offsets]

def count_neighbours(point, points):
    return sum(map(lambda x: x in points, get_neighbours(point)))

def get_bounds(points):
    return add_vectors(tuple(map(min, zip(*points))), (-1,-1,-1)), add_vectors(tuple(map(max, zip(*points))), (1,1,1))

def within_region(point, lower_bound, upper_bound):
    return all(lower_bound[i] <= point[i] <= upper_bound[i] for i in range(len(point)))

def get_reachable_points(points):
    bounds = get_bounds(points)
    reachable_points = {bounds[0]}
    queue = [bounds[0]]
    while len(queue) != 0:
        for neighbour in get_neighbours(queue.pop(0)):
            if neighbour not in points and neighbour not in reachable_points and within_region(neighbour, *bounds):
                reachable_points.add(neighbour)
                queue.append(neighbour)
    return reachable_points

def get_surface_area(points):
    return sum(6 - count_neighbours(point, points) for point in points)

def get_reachable_surface_area(points):
    reachable_points = get_reachable_points(points)
    return sum(count_neighbours(point, reachable_points) for point in points)

def main():
    with open("Inputs/Day18.txt") as file:
        points = set(map(eval, file.read().splitlines()))
    print(get_surface_area(points))
    print(get_reachable_surface_area(points))

main()