input_file = open("input.txt", "r")
line = input_file.readline().strip()

def part_1(input):
    polymer_chain = list()
    for char in input:
        if len(polymer_chain) > 0:
            previous_char = polymer_chain[-1]
            if previous_char.lower() == char.lower() and previous_char.isupper() != char.isupper():
                polymer_chain.pop()
            else:
                polymer_chain.append(char)
        else:
            polymer_chain.append(char)

    reduced_chain = ""
    for char in polymer_chain:
        reduced_chain += char
    print(f"chain is reduced to {reduced_chain}")
    print(f"{len(polymer_chain)} units remain")
    return len(polymer_chain)

def part_2(input):
    smallest_length = len(input)
    best_reduction = ""
    for char in "abcdefghijklmnopqrstuvwxyz":
        improved_polymer = input.replace(char, "").replace(char.upper(), "")
        print(f"running part 2 by removing {char}")
        print(f"length of improved polymer is {len(improved_polymer)}")
        improved_length = part_1(improved_polymer)
        if improved_length < smallest_length:
            smallest_length = improved_length
            best_reduction = char
    print(f"The smallest length is {smallest_length}")
    print(f"The best character to remove is {best_reduction}")

part_2(line)