import re
import tkinter
import time


class Point:
    def __init__(self, starting_x, starting_y, x_velocity, y_velocity) -> None:
        super().__init__()
        self.x = starting_x
        self.y = starting_y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def get_position(self):
        return self.x, self.y


class Grid:

    def __init__(self, starting_points) -> None:
        super().__init__()
        self.points = starting_points

    def get_point_set(self):
        positions = set()
        for point in self.points:
            positions.add((point.x, point.y))
        return positions

    def draw_grid(self):
        # find grid bounds
        min_x = 10000
        min_y = 10000
        max_x = -10000
        max_y = -10000
        for point in self.points:
            if point.x < min_x:
                min_x = point.x
            elif point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            elif point.y > max_y:
                max_y = point.y

        output_str = ""
        positions = self.get_point_set()
        for row in range(min_y, max_y + 1):
            for col in range(min_x, max_x + 1):
                if (col, row) in positions:
                    output_str += "#"
                else:
                    output_str += " "
            print(output_str)
            output_str = ""
        print("-----------------------------------------------------------------------")

    def move_points(self):
        for point in self.points:
            point.move()


class Sky:

    def __init__(self, starting_points, width, height) -> None:
        super().__init__()
        self.points = starting_points
        self.dots = list()
        self.gui = tkinter.Tk()
        self.canvas_width = width
        self.canvas_height = height
        self.canvas = tkinter.Canvas(self.gui, width=self.canvas_width, height=self.canvas_height, bg="blue")
        self.canvas.pack()

    def get_bounds(self):
        # find grid bounds
        min_x = self.points[0].x
        min_y = self.points[0].y
        max_x = self.points[0].x
        max_y = self.points[0].y
        for point in self.points:
            if point.x < min_x:
                min_x = point.x
            elif point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            elif point.y > max_y:
                max_y = point.y
        return min_x, min_y, max_x, max_y

    def draw_dots(self):
        min_x, min_y, max_x, max_y = self.get_bounds()
        points_width = max_x - min_x
        points_height = max_y - min_y
        horizontal_scale_factor = points_width / self.canvas_width
        vertical_scale_factor = points_height / self.canvas_height
        scale_factor = max(horizontal_scale_factor, vertical_scale_factor)

        self.canvas.delete("all")
        for point in self.points:
            circle_center_x = (point.x - min_x) / scale_factor
            circle_center_y = (point.y - min_y) / scale_factor
            radius = 10
            self.canvas.create_oval(
                circle_center_x - radius,
                circle_center_y - radius,
                circle_center_x + radius,
                circle_center_y + radius,
                fill="red"
            )
        self.gui.update()

    def move_dots(self, start, end, step=1):
        for i in range(start):
            for point in self.points:
                point.move()

        for i in range(start, end, step):
            for j in range(step):
                for point in self.points:
                    point.move()
            self.draw_dots()
            print(f"animated at {i} iterations")
            time.sleep(0.1)

    def animate(self):
        self.gui.mainloop()


# tick through seconds and redraw the grid
def extract_points(filename):
    input_file = open(filename, "r")
    input_lines = input_file.readlines()
    pattern = r"position=<(-?\s?\d+?),\s(-?\s?\d+?)> velocity=<(-?\s?\d+?),\s(-?\s?\d+?)>"
    points = list()
    for line in input_lines:
        line = line.strip()
        matches = re.search(pattern, line)
        points.append(Point(
            int(matches.group(1)),
            int(matches.group(2)),
            int(matches.group(3)),
            int(matches.group(4))
        ))
    return points


def part1_example():
    grid = Grid(extract_points("example_input.txt"))
    grid.draw_grid()
    for i in range(3):
        grid.move_points()
        grid.draw_grid()


def part1_problem():
    sky = Sky(extract_points("input.txt"), 500,  500)
    sky.draw_dots()
    sky.move_dots(10800, 10831, 1)
    sky.animate()


# part1_example()
part1_problem()

# Answer to part 1 is BHPJGLPE
# Answer to part 2 10831 seconds
