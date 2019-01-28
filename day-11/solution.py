class PowerCellGrid:
    def __init__(self, width, height, serial_number):
        self.grid = list()
        for y in range(1, height+1):
            self.grid.append(list())
            for x in range(1, width+1):
                self.grid[y-1].append(self.find_power_level(x, y, serial_number))

    def find_power_level(self, x, y, serial_number):
        # Find the fuel cell's rack ID, which is its X coordinate plus 10.
        rack_id = x + 10
        # Begin with a power level of the rack ID times the Y coordinate.
        power_level = rack_id * y
        # Increase the power level by the value of the grid serial number (your puzzle input).
        power_level += serial_number
        # Set the power level to itself multiplied by the rack ID.
        power_level *= rack_id
        # Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
        power_level = (power_level // 100) % 10
        # Subtract 5 from the power level.
        power_level -= 5
        return power_level

    def find_max_3_square(self):
        max_power_level = 0
        max_location = (0, 0)
        for y in range(len(self.grid) - 3):
            for x in range(len(self.grid[y]) - 3):
                square_power_level = self.power_level_3_square(x, y)
                if square_power_level > max_power_level:
                    max_power_level = square_power_level
                    max_location = (x + 1, y + 1)
        print(f"Max Power Level is {max_power_level}")
        print(f"Max Location is {max_location}")

    def power_level_3_square(self, x, y):
        square_sum = 0
        for row in range(x, x + 3):
            for col in range(y, y + 3):
                square_sum += self.grid[col][row]
        return square_sum

    def find_max_square(self):
        max_power_level = 0
        max_power_size = 0
        max_location = (0, 0)
        for size in range(1, len(self.grid) + 1):
            for y in range(len(self.grid) - size + 1):
                for x in range(len(self.grid[y]) - size + 1):
                    square_power_level = self.power_level_square(x, y, size)
                    if square_power_level > max_power_level:
                        max_power_level = square_power_level
                        max_power_size = size
                        max_location = (x + 1, y + 1)
            print(f"Calculated max for size {size}")
        print(f"Max Power Level is {max_power_level}")
        print(f"Max Location is {max_location}")
        print(f"Square size is {max_power_size}")

    def find_max_square_optimized(self):
        max_power_level = 0
        max_power_size = 0
        max_location = (0, 0)
        previous_square_sums = self.grid.copy()
        for size in range(2, len(self.grid) + 1):
            nested_square_sums = list()
            local_max_power_level = -9999999999999999
            local_max_location = (0, 0)
            for y in range(len(previous_square_sums) - 1):
                nested_square_sums.append(list())
                for x in range(len(previous_square_sums) - 1):
                    square_power_level = self.find_square_sum(x, y, size, previous_square_sums)
                    nested_square_sums[y].append(square_power_level)
                    if square_power_level > local_max_power_level:
                        local_max_power_level = square_power_level
                        local_max_location = (x + 1, y + 1)
                    if square_power_level > max_power_level:
                        max_power_level = square_power_level
                        max_power_size = size
                        max_location = (x + 1, y + 1)
            previous_square_sums = nested_square_sums
            print(f"Calculated size {size}")
            print(f"Local Max Power Level is {local_max_power_level}")
            print(f"Local Max Power Location is {local_max_location}")
            print(f"Best Square size is {max_power_size}")
            print(f"Max Power Level is {max_power_level}")
            print(f"Max Location is {max_location}")

    def find_square_sum(self, x, y, size, previous_square_sums):
        nested_square = previous_square_sums[y][x]
        square_sum = nested_square
        # add the column to the right
        for row in range(y, y + size):
            square_sum += self.grid[row][x + size - 1]
        for col in range(x, x + size):
            square_sum += self.grid[y + size - 1][col]
        square_sum -= self.grid[y + size - 1][x + size - 1]
        return square_sum

    def power_level_square(self, x, y, size):
        square_sum = 0
        for row in range(x, x + size):
            for col in range(y, y + size):
                square_sum += self.grid[col][row]
        return square_sum

    def pretty_print(self):
        for i in range(len(self.grid)):
            print(self.grid[i])


grid = PowerCellGrid(300, 300, 4151)
# Part 1
grid.find_max_3_square()
# Part 2
# grid.find_max_square()
grid.find_max_square_optimized()

