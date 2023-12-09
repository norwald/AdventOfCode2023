from functools import reduce
from math import gcd

from SolverBase import SolverBase


def lcm(numbers):
    return reduce((lambda x, y: int(x * y / gcd(x, y))), numbers)


class PathNode:
    def __init__(self, string_raw):
        string_split = string_raw.strip().split("=")
        neighbors = string_split[1].strip().split(",")

        self.my_name = string_split[0].strip()
        self.left_name = neighbors[0].strip()[1:4]
        self.right_name = neighbors[1].strip()[0:3]


class PathMap:
    def __init__(self, input_lines):
        non_empty_lines = [line for line in input_lines if line.strip()]

        self.instructions = non_empty_lines[0]
        self.path_nodes_lookup = {}
        self.next_instruction = 0

        for line in non_empty_lines[1:]:
            node = PathNode(line)
            self.path_nodes_lookup[node.my_name] = node

    def find_path(self):
        current_node = self.path_nodes_lookup['AAA']

        full_path = [current_node]

        while True:
            current_instruction = self.get_next_instruction()
            if current_instruction == "L":
                current_node = self.path_nodes_lookup[current_node.left_name]
            else:
                current_node = self.path_nodes_lookup[current_node.right_name]

            full_path.append(current_node)
            if current_node.my_name == 'ZZZ':
                return full_path

    # brute force does not work
    def find_ghost_path(self):
        current_path_nodes = [item[1] for item in self.path_nodes_lookup.items() if item[0].endswith('A')]

        full_path_steps_count = 1
        while True:
            current_instruction = self.get_next_instruction()
            current_path_nodes = self.visit_simultaneously(current_path_nodes.copy(), current_instruction)

            full_path_steps_count += 1
            if all(node.my_name[2] == 'Z' for node in current_path_nodes):
                return full_path_steps_count

    def visit_simultaneously(self, path_nodes, instruction):
        next_path_nodes = []
        for path_node in path_nodes:
            if instruction == 'L':
                next_path_nodes.append(self.path_nodes_lookup[path_node.left_name])
            else:
                next_path_nodes.append(self.path_nodes_lookup[path_node.right_name])

        print(" ".join([name.my_name for name in next_path_nodes]))
        return next_path_nodes

    def find_cycles_to_finish(self):
        all_nodes_cycles = []
        current_path_nodes = [item[1] for item in self.path_nodes_lookup.items() if item[0].endswith('A')]

        for node in current_path_nodes:
            self.reset_next_instruction()
            all_nodes_cycles.append(self.find_steps_to_finish(node))

        return all_nodes_cycles

    def find_steps_to_finish(self, current_node):
        number_of_steps = 0
        while True:
            number_of_steps += 1
            current_instruction = self.get_next_instruction()
            if current_instruction == "L":
                current_node = self.path_nodes_lookup[current_node.left_name]
            else:
                current_node = self.path_nodes_lookup[current_node.right_name]

            if current_node.my_name[2] == 'Z':
                return number_of_steps

    def reset_next_instruction(self):
        self.next_instruction = 0

    def get_next_instruction(self):
        current = self.next_instruction
        if current == len(self.instructions):
            self.next_instruction = 0
            current = 0

        self.next_instruction += 1
        return self.instructions[current]


class Problem1(SolverBase):

    def solve(self):
        path_map = PathMap(self.input_data)
        print(len(path_map.find_path()) - 1)


class Problem2(SolverBase):

    def solve(self):
        path_map = PathMap(self.input_data)
        cycles = path_map.find_cycles_to_finish()
        result = lcm(cycles)

        print(cycles)
        print(result)


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
