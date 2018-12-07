import collections
input_file = open("input.txt", "r")
lines = input_file.readlines()


def part_1():
    twice_repeating_counter = 0 #abccde
    three_repeating_counter = 0 #abcccd
    for line in lines:
        char_counter = collections.defaultdict(int)
        for char in line.strip():
            char_counter[char] += 1
        frequency_set = set(char_counter.values())
        if 2 in frequency_set:
            twice_repeating_counter += 1
        if 3 in frequency_set:
            three_repeating_counter += 1
    print(twice_repeating_counter * three_repeating_counter)


def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def find_strings_of_distance_1(lines):
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            line1 = lines[i].strip()
            line2 = lines[j].strip()
            if hamming_distance(line1, line2) == 1:
                return line1, line2
    return None


def part_2():
    line1, line2 = find_strings_of_distance_1(lines)

    # Make a new string with all common characters of line 1 and line 2
    line3 = ""
    for i in range(len(line1)):
        if line1[i] == line2[i]:
            line3 += line1[i]

    print(line3)


# part_1()
part_2()
