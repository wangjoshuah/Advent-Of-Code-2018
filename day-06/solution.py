from collections import defaultdict


def manhattan_distance(point1, point2):
    x_distance = abs(point1[0] - point2[0])
    y_distance = abs(point1[1] - point2[1])
    return x_distance + y_distance


def find_nearest_coordinate(point, coordinates):
    min_distance = 1000
    closest_coordinate = None
    for coordinate in coordinates:
        distance = manhattan_distance(point, coordinate)
        if distance == 0:
            return coordinate
        elif distance < min_distance:
            min_distance = distance
            closest_coordinate = coordinate
        elif distance == min_distance:
            closest_coordinate = None
    return closest_coordinate


# True if total distance of point to all coordinates is less than max_distance
# False if total distance of point to all coordinates is greater than max_distance
def point_within_range_of_coordinates(point, max_distance, coordinates):
    total_distance = 0
    for coordinate in coordinates:
        total_distance += manhattan_distance(point, coordinate)
        if total_distance >= max_distance:
            return False

    return True


class Solution:
    def __init__(self) -> None:
        input_file = open("input.txt", "r")
        input_lines = input_file.readlines()
        # Make a list of all coordinates to iterate over
        # Make our grid of (minx, miny) to (max x, max y) / define bounds
        self.input_coordinates = list()
        self.min_x = 500
        self.min_y = 500
        self.max_x = 0
        self.max_y = 0
        for line in input_lines:
            x_str, y_str = line.strip().split(", ")
            x = int(x_str)
            y = int(y_str)
            self.input_coordinates.append((x, y))
            if x < self.min_x:
                self.min_x = x
            elif x > self.max_x:
                self.max_x = x
            if y < self.min_y:
                self.min_y = y
            elif y > self.max_y:
                self.max_y = y

    def part_1(self):
        # Dict of {Coordinate : set of points in its area}
        areas = defaultdict(set)
        infinite_areas = set()
        finite_areas = set()

        # for each point in the grid, find the closest coordinate
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                nearest_coordinate = find_nearest_coordinate((x, y), self.input_coordinates)
                # Count up points in a coordinate's area in a set
                if nearest_coordinate is not None:
                    areas[nearest_coordinate].add((x, y))
                    if x == self.min_x or x == self.max_x or y == self.min_y or y == self.max_y:
                        infinite_areas.add(nearest_coordinate)

            # Find all areas that are finite (no points on edge of grid)
            finite_areas = set(self.input_coordinates) - infinite_areas

        # Find largest set of points
        max_area = 0
        for finite_area in finite_areas:
            area = len(areas[finite_area])
            if area > max_area:
                max_area = area

        print(f"max_area is {max_area}")

    def part_2(self):
        # find set of all points with total distance to all coordinates < 10000
        desired_region = set()
        max_distance = 10000
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                # if point is in desired region: add to set
                point = (x, y)
                if point_within_range_of_coordinates(point, max_distance, self.input_coordinates):
                    desired_region.add(point)

        # return size of set
        print(f"desired region is made up of {desired_region}")
        return len(desired_region)


solution = Solution()
print(solution.part_2())





