from abc import ABC, abstractmethod


class SolverBase(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath) as file:
            self.content = [line.strip() for line in file.readlines()]

    @abstractmethod
    def solve(self):
        pass


