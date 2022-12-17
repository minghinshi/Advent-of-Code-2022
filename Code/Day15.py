class sensor:
    def __init__(self, line) -> None:
        self.position, self.beacon_position = parse_line(line)
        self.range = get_manhattan_distance(self.position, self.beacon_position)

    def get_no_beacon_range(self, row):
        vertical_distance = abs(self.position[1] - row)
        difference = self.range - vertical_distance
        return self.position[0] - difference, self.position[0] + difference + 1

    def get_no_beacon_set(self, row):
        return set(range(*self.get_no_beacon_range(row)))

    def in_range(self, other):
        return get_manhattan_distance(self.position, other) <= self.range

def parse_coordinate(line: str):
    strings = line.split(", ")
    return int(strings[0].removeprefix("x=")), int(strings[1].removeprefix("y="))

def parse_line(line: str):
    line = line.replace("Sensor at ", "").replace("closest beacon is at ", "")
    strings = line.split(": ")
    return parse_coordinate(strings[0]), parse_coordinate(strings[1])

def get_sensors():
    with open("Inputs/Day15.txt") as file:
        return [sensor(line) for line in file]

def get_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def get_all_no_beacon_range(sensors: list[sensor], row):
    no_beacon_range = set()
    for sensor in sensors:
        no_beacon_range.update(sensor.get_no_beacon_set(row))
    for sensor in sensors:
        beacon_x, beacon_y = sensor.beacon_position
        if beacon_y == row and beacon_x in no_beacon_range:
            no_beacon_range.remove(beacon_x)
    return no_beacon_range

def get_sensor_in_range(sensors: list[sensor], position):
    for sensor in sensors:
        if sensor.in_range(position):
            return sensor

def get_missing_beacon(sensors: list[sensor], max_coord):
    for y in range(max_coord + 1):
        x = 0
        while x < max_coord + 1:
            sensor = get_sensor_in_range(sensors, (x, y))
            if sensor is None:
                return x, y
            x = sensor.get_no_beacon_range(y)[1]

def main():
    sensors = get_sensors()
    print(len(get_all_no_beacon_range(sensors, 2000000)))
    print(get_missing_beacon(sensors, 4000000))

main()