from abc import ABC, abstractmethod


class SolverBase(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath) as file:
            self.input_data = [line.strip() for line in file.readlines()]

    def find_empty_indices(self):
        empty_indices = []
        for counter in range(len(self.input_data)):
            if not self.input_data[counter]:
                empty_indices.append(counter)
        return empty_indices

    @abstractmethod
    def solve(self):
        pass


