import queue

from SolverBase import SolverBase


class Pipe:
    pipe_symbols = {"|", "-", "L", "J", "7", "F", "S"}

    @staticmethod
    def empty():
        return Pipe(".", (-1, -1))

    def __init__(self, symbol, offset_indices):
        self.symbol = symbol
        self.offset_indices = offset_indices
        self.possible_neighbours_indices = []
        self.__eval_possible_neighbours_indices()

    def is_start(self):
        return self.symbol == "S"

    def is_pipe(self):
        return self.symbol in Pipe.pipe_symbols

    def is_actual_neighbour(self, other_pipe):
        return self.offset_indices in other_pipe.possible_neighbours_indices

    def __eval_possible_neighbours_indices(self):
        if self.symbol == "|":
            self.possible_neighbours_indices.append((self.offset_indices[0] + 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0] - 1, self.offset_indices[1]))
        elif self.symbol == "-":
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] + 1))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] - 1))
        elif self.symbol == "L":
            self.possible_neighbours_indices.append((self.offset_indices[0] - 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] + 1))
        elif self.symbol == "J":
            self.possible_neighbours_indices.append((self.offset_indices[0] - 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] - 1))
        elif self.symbol == "7":
            self.possible_neighbours_indices.append((self.offset_indices[0] + 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] - 1))
        elif self.symbol == "F":
            self.possible_neighbours_indices.append((self.offset_indices[0] + 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] + 1))
        elif self.symbol == "S":
            self.possible_neighbours_indices.append((self.offset_indices[0] + 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0] - 1, self.offset_indices[1]))

            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] + 1))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] - 1))

            self.possible_neighbours_indices.append((self.offset_indices[0] - 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] + 1))

            self.possible_neighbours_indices.append((self.offset_indices[0] - 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] - 1))

            self.possible_neighbours_indices.append((self.offset_indices[0] + 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] - 1))

            self.possible_neighbours_indices.append((self.offset_indices[0] + 1, self.offset_indices[1]))
            self.possible_neighbours_indices.append((self.offset_indices[0], self.offset_indices[1] + 1))


class PipeMaze:
    def __init__(self, input_lines):
        self.horizontal_len = len(input_lines[0])
        self.vertical_len = len(input_lines)
        self.maze = []

        for vertical_counter in range(0, len(input_lines)):
            line = input_lines[vertical_counter]

            horizontal_path = []
            for horizontal_counter in range(0, len(line)):
                horizontal_path.append(Pipe(line[horizontal_counter], (vertical_counter, horizontal_counter)))

            self.maze.append(horizontal_path)

    def traverse_pipes(self):
        start = self.find_starting_pipe()
        pipes_to_visit = queue.LifoQueue()
        pipes_to_visit.put(start.offset_indices)

        visited_pipes = set()
        while not pipes_to_visit.empty():
            to_visit_index = pipes_to_visit.get()
            to_visit_pipe = self.maze[to_visit_index[0]][to_visit_index[1]]
            if self.is_pipe_in_maze(to_visit_index) and to_visit_index not in visited_pipes:
                print("Symbol {} row {} column {}".format(to_visit_pipe.symbol,
                                                          to_visit_pipe.offset_indices[0], to_visit_pipe.offset_indices[1]))
                visited_pipes.add(to_visit_index)
                for neighbor_index in to_visit_pipe.possible_neighbours_indices:
                    if to_visit_pipe.is_pipe() and to_visit_pipe.is_actual_neighbour(self.maze[neighbor_index[0]][neighbor_index[1]]):
                        pipes_to_visit.put(neighbor_index)

        return visited_pipes

    def is_pipe_in_maze(self, pipe_index):
        return 0 <= pipe_index[0] < self.vertical_len and 0 <= pipe_index[1] < self.horizontal_len

    def find_starting_pipe(self) -> Pipe:
        for vertical_counter in range(0, self.vertical_len):
            for horizontal_counter in range(0, self.horizontal_len):
                if self.maze[vertical_counter][horizontal_counter].is_start():
                    return self.maze[vertical_counter][horizontal_counter]

        return Pipe.empty()


class Problem1(SolverBase):
    def solve(self):
        maze = PipeMaze(self.input_data)
        print(maze.find_starting_pipe().offset_indices)
        route_indices  = maze.traverse_pipes()
        print(len(route_indices)/2)


problem1 = Problem1("Input.txt")
problem1.solve()