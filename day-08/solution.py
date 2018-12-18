input_file = open("input.txt", "r")
input_values = input_file.readline().split(" ")


class Node:

    def __init__(self, input_stream) -> None:
        super().__init__()
        self.children = []
        self.metadata = []
        self.num_children = int(input_stream.pop(0))
        self.num_metadata = int(input_stream.pop(0))
        for i in range(self.num_children):
            self.children.append(Node(input_stream))
        for i in range(self.num_metadata):
            self.metadata.append(int(input_stream.pop(0)))

    def get_metadata_sum(self):
        sum = 0
        for metadata in self.metadata:
            sum += metadata
        for child in self.children:
            sum += child.get_metadata_sum()
        return sum

    def get_value(self):
        if self.num_children == 0:
            return self.get_metadata_sum()
        else:
            value_sum = 0
            for metadata in self.metadata:
                if metadata <= self.num_children:
                    child = self.children[metadata - 1]
                    if child is not None:
                        value_sum += child.get_value()
            return value_sum


root = Node(input_values)
print(root.get_metadata_sum())
print(root.get_value())
