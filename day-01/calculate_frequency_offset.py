input_file = open("input.txt", "r")

def part_1():
    sum = 0
    for line in input_file.readlines():
        sum += int(line.strip())
    print(sum)

def part_2():
    sum = 0
    numbers_seen = set()
    iterations = 0
    lines = input_file.readlines()
    while sum not in numbers_seen:
        for line in lines:
            numbers_seen.add(sum)
            sum += int(line.strip())
            print("current sum is ", sum)
            if sum in numbers_seen:
                print("The first number seen is ", sum)
                return sum
            iterations += 1
            print("Iterations: ", iterations)
            print("Size of numbers seen: ", len(numbers_seen))

part_2()