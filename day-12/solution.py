import re

CHECK_RANGE = 2 # floor rule length / 2

class Pot:
    def __init__(self, has_plant=False):
        self.has_plant = has_plant
        self.left = None
        self.right = None

    def get_configuration(self):
        configuration = ""
        if self.left and self.left.left and self.left.left.has_plant:
            configuration += "#"
        else:
            configuration += "."
        if self.left and self.left.has_plant:
            configuration += "#"
        else:
            configuration += "."
        if self.has_plant:
            configuration += "#"
        else:
            configuration += "."
        if self.right and self.right.has_plant:
            configuration += "#"
        else:
            configuration += "."
        if self.right and self.right.right and self.right.right.has_plant:
            configuration += "#"
        else:
            configuration += "."
        return configuration

    def will_have_plant(self, rules):
        configuration = self.get_configuration()
        if configuration in rules:
            return True
        else:
            return False

    def set_right(self, other_pot):
        self.right = other_pot
        other_pot.left = self

    def set_left(self, other_pot):
        self.left = other_pot
        other_pot.right = self

    def pop_from_end(self):
        if self.right:
            self.right.left = None
        if self.left:
            self.left.right = None


class Tunnel:
    def __init__(self, initial_state_string, rules_map, verbose=False):
        self.zero_pot = Pot(True if initial_state_string[0] is "#" else False)
        self.head = self.zero_pot
        current_pot = self.zero_pot
        for i in range(1, len(initial_state_string)):
            new_pot = Pot(True if initial_state_string[i] is "#" else False)
            current_pot.set_right(new_pot)
            current_pot = current_pot.right
        self.rules = rules_map
        self.verbose = verbose
        self.generations = 0

    def print_tunnel(self):
        current_pot = self.head
        tunnel_string = ""
        while current_pot:
            tunnel_string += "#" if current_pot.has_plant else "."
            current_pot = current_pot.right
        print(tunnel_string)

    def next_generation(self):
        current_pot = self.zero_pot
        next_generation_zero = Pot(self.zero_pot.will_have_plant(self.rules))
        next_gen_current = next_generation_zero
        # go left to end of current pots
        while current_pot.left:
            current_pot = current_pot.left
            new_pot = Pot(current_pot.will_have_plant(self.rules))
            next_gen_current.set_left(new_pot)
            next_gen_current = new_pot
        # check if new pots will be made on the left
        for i in range(CHECK_RANGE):
            current_pot.set_left(Pot())
            current_pot = current_pot.left
            new_pot = Pot(current_pot.will_have_plant(self.rules))
            next_gen_current.set_left(new_pot)
            next_gen_current = new_pot
        # trim left if they are all empty
        while not next_gen_current.has_plant and next_gen_current is not next_generation_zero:
            next_gen_current.pop_from_end()
            next_gen_current = next_gen_current.right
        self.head = next_gen_current

        current_pot = self.zero_pot
        next_gen_current = next_generation_zero
        # go right
        while current_pot.right:
            current_pot = current_pot.right
            new_pot = Pot(current_pot.will_have_plant(self.rules))
            next_gen_current.set_right(new_pot)
            next_gen_current = new_pot
        # check if new pots will be made on the right
        for i in range(CHECK_RANGE):
            current_pot.set_right(Pot())
            current_pot = current_pot.right
            new_pot = Pot(current_pot.will_have_plant(self.rules))
            next_gen_current.set_right(new_pot)
            next_gen_current = new_pot
        # trim right if they are all empty
        while not next_gen_current.has_plant and next_gen_current is not next_generation_zero:
            next_gen_current.pop_from_end()
            next_gen_current = next_gen_current.left

        # prepare the next gen
        self.zero_pot = next_generation_zero
        self.generations += 1
        if self.verbose:
            self.print_tunnel()
        print("Grew " + str(self.generations) + " generations.")
        print("Pot sum is " + str(self.sum_pots()))

    def sum_pots(self):
        sum = 0
        # go left
        current_pot = self.zero_pot
        counter = 0
        while current_pot.left:
            current_pot = current_pot.left
            counter -= 1
            if current_pot.has_plant:
                sum += counter

        # go right
        current_pot = self.zero_pot
        counter = 0
        while current_pot.right:
            current_pot = current_pot.right
            counter += 1
            if current_pot.has_plant:
                sum += counter
        return sum


def parse_input(filename):
    input_file = open(filename, "r")
    initial_state_pattern = r"initial state: ([#|\.]+)"
    initial_state_search = re.search(initial_state_pattern, input_file.readline())
    initial_state_string = initial_state_search.group(1)
    input_file.readline()
    line = input_file.readline()
    rule_pattern = r"([#|\.]{5}) => (#|\.){1}"
    rules = {}
    while line:
        rule_search = re.search(rule_pattern, line)
        if rule_search.group(2) is "#":
            rules[rule_search.group(1)] = rule_search.group(2)
        line = input_file.readline()
    return Tunnel(initial_state_string, rules)


# part 1
def part_1():
    tunnel = parse_input("input.txt")
    tunnel.verbose = True
    tunnel.print_tunnel()
    for i in range(20):
        tunnel.next_generation()
    print(tunnel.sum_pots())


def part_2():
    tunnel = parse_input("input.txt")
    tunnel.print_tunnel()
    for i in range(50000000000):
        tunnel.next_generation()
    print(tunnel.sum_pots())


# answer 2,550,000,001,195
part_2()
