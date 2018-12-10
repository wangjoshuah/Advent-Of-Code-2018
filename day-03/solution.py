from collections import defaultdict

input_file = open("input.txt", "r")
lines = input_file.readlines()

def extract_parameters(line):
    split_on_space = line.strip("#").split(' ')
    claim_id = int(split_on_space[0])
    locations = split_on_space[2].strip(":").split(",")
    x = int(locations[0])
    y = int(locations[1])
    size = split_on_space[3].split("x")
    width = int(size[0])
    height = int(size[1])
    return claim_id, x, y, width, height


def part_1():
    num_claims_on_location = defaultdict(int)
    area_claimed_by_at_least_two = 0
    for line in lines:
        claim_id, x, y, width, height = extract_parameters(line.strip())
        for i in range(width):
            for j in range(height):
                point = (x + i, y + j)
                num_claims_on_location[point] += 1
                if num_claims_on_location[point] == 2:
                    area_claimed_by_at_least_two += 1

    print("Area claimed by at least two claims is ")
    print(area_claimed_by_at_least_two)

def part_2():
    claims_on_location = defaultdict(set)
    possible_unique_claims = set()
    definitely_not_unique_claims = set()
    for line in lines:
        claim_id, x, y, width, height = extract_parameters(line.strip())
        for i in range(width):
            for j in range(height):
                point = (x + i, y + j)
                claims = claims_on_location[point]
                claims.add(claim_id)
                claims_on_location[point] = claims
                if len(claims) == 1:
                    possible_unique_claims.add(claim_id)
                elif len(claims) > 1:
                    for claim in claims:
                        definitely_not_unique_claims.add(claim)

    print(possible_unique_claims.difference(definitely_not_unique_claims))


part_2()
