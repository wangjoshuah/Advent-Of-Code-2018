# directed graph problem or breadth first search variant
from collections import defaultdict
import re

input_file = open("input.txt", "r")
input_lines = input_file.readlines()

letter_value = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
    'K': 11,
    'L': 12,
    'M': 13,
    'N': 14,
    'O': 15,
    'P': 16,
    'Q': 17,
    'R': 18,
    'S': 19,
    'T': 20,
    'U': 21,
    'V': 22,
    'W': 23,
    'X': 24,
    'Y': 25,
    'Z': 26
}


# construct graph of nodes and edges
# Read nodes and edges from input with regex
def construct_graph(lines):
    # Graph is a Dictionary of String to Set
    # { Node : Set of children }
    edges = defaultdict(set)
    nodes = set()
    pattern = r"Step (.?) must be finished before step (.?) can begin\."
    for line in lines:
        matches = re.search(pattern, line)
        edges[matches.group(1)].add(matches.group(2))
        nodes.add(matches.group(1))
        nodes.add(matches.group(2))
    return nodes, edges


# A set of possible nodes to work on (starts with C)
# pick the first alphabetical node and remove it and its edges
def find_all_nodes_to_work(nodes, edges):
    possible_nodes_to_work = nodes.copy()
    for parent, children in edges.items():
        for child in children:
            if child in possible_nodes_to_work:
                possible_nodes_to_work.remove(child)

    sorted_work = list(possible_nodes_to_work)
    sorted_work.sort()
    return sorted_work


def find_next_node_to_work(nodes, edges):
    return find_all_nodes_to_work(nodes, edges)[0]


def work_nodes(nodes, edges):
    work_order = ""
    while len(nodes) > 0:
        node_to_work = find_next_node_to_work(nodes, edges)
        nodes.remove(node_to_work)
        if node_to_work in edges:
            del edges[node_to_work]
        work_order += node_to_work
    return work_order


class Worker:
    def __init__(self, base_time) -> None:
        super().__init__()
        self.current_node = None
        self.seconds_left = 0
        self.free = True
        self.base_time = base_time

    def assign(self, node):
        self.current_node = node
        self.seconds_left = letter_value[node] + self.base_time
        self.free = False

    def tick(self):
        self.seconds_left -= 1
        if self.seconds_left <= 0:
            finished_node = self.current_node
            self.current_node = None
            self.free = True
            self.seconds_left = 0
            return finished_node


def work_nodes_in_parallel(nodes, edges, workers, base_time):
    timer = 0
    worker_pool = list()
    nodes_worked = set()
    for i in range(workers):
        worker_pool.append(Worker(base_time))
    while len(nodes) > 0:
        print(f"Second {timer}")
        nodes_to_work = find_all_nodes_to_work(nodes, edges)
        for node in nodes_to_work:
            if node not in nodes_worked:
                for worker in worker_pool:
                    if worker.free and node not in nodes_worked:
                        worker.assign(node)
                        nodes_worked.add(node)
        for worker in worker_pool:
            print(f"Worker is working on {worker.current_node} with {worker.seconds_left} seconds left.")
            finished_node = worker.tick()
            if finished_node is not None:
                # if a worker finishes a node
                nodes.remove(finished_node)
                nodes_worked.remove(finished_node)
                if finished_node in edges:
                    del edges[finished_node]
        timer += 1
    return timer


# Part 1
# print(work_nodes(construct_graph(input_lines)))

# Part 2
nodes, edges = construct_graph(input_lines)
total_time = work_nodes_in_parallel(nodes, edges, 5, 60)
print(f"It took {total_time} seconds")

