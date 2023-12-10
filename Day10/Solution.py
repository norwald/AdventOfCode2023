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
            to_visit_indices = pipes_to_visit.get()
            to_visit_pipe = self.maze[to_visit_indices[0]][to_visit_indices[1]]
            if self.is_pipe_in_maze(to_visit_indices) and to_visit_indices not in visited_pipes:
                print("Symbol {} row {} column {}".format(to_visit_pipe.symbol,
                                                          to_visit_pipe.offset_indices[0],
                                                          to_visit_pipe.offset_indices[1]))
                visited_pipes.add(to_visit_indices)
                for neighbor_indices in to_visit_pipe.possible_neighbours_indices:
                    if to_visit_pipe.is_pipe() and to_visit_pipe.is_actual_neighbour(
                            self.maze[neighbor_indices[0]][neighbor_indices[1]]):
                        pipes_to_visit.put(neighbor_indices)

        return visited_pipes

    def is_pipe_in_maze(self, pipe_indices):
        return 0 <= pipe_indices[0] < self.vertical_len and 0 <= pipe_indices[1] < self.horizontal_len

    def find_starting_pipe(self) -> Pipe:
        for vertical_counter in range(0, self.vertical_len):
            for horizontal_counter in range(0, self.horizontal_len):
                if self.maze[vertical_counter][horizontal_counter].is_start():
                    return self.maze[vertical_counter][horizontal_counter]

        return Pipe.empty()

    def visit_non_pipe_tiles(self):
        pipes_in_loop = self.traverse_pipes()
        full_maze = set([(vertical, horizontal) for vertical in range(0, self.vertical_len)
                         for horizontal in range(0, self.horizontal_len)])
        tiles_not_in_loop = full_maze - pipes_in_loop
        print(len(full_maze))
        print(len(pipes_in_loop))
        print(len(tiles_not_in_loop))


class PipeMazeSniffer:
    def __init__(self, pipe_maze):
        self.maze = pipe_maze.maze
        self.horizontal_len = pipe_maze.horizontal_len + 2
        self.vertical_len = pipe_maze.vertical_len + 2
        self.full_maze = set([(vertical, horizontal) for vertical in range(-1, pipe_maze.horizontal_len + 1)
                              for horizontal in range(-1, pipe_maze.vertical_len + 1)])
        self.pipes_in_loop = pipe_maze.traverse_pipes()
        self.tiles_not_in_loop = self.full_maze.difference(self.pipes_in_loop)

    def find_all_outside_tiles(self):
        starting_index = (-1, -1)
        tiles_to_visit = queue.Queue()
        visited_tiles = set()

        tiles_to_visit.put(starting_index)

        while not tiles_to_visit.empty():
            current_tile = tiles_to_visit.get()
            if current_tile not in visited_tiles:
                visited_tiles.add(current_tile)
                for neighbour in self.get_passable_neighbours(current_tile):
                    tiles_to_visit.put(neighbour)



    def get_passable_neighbours(self, tile_indices):
        neighbours = []



        return neighbours

    def can_move_right(self, tile_indices):
        if tile_indices[1] + 1 >= self.horizontal_len:
            return False
        if tile_indices[0] == -1 or tile_indices[0] == self.vertical_len - 1:
            return True
        if (tile_indices[0], tile_indices[1] + 1) not in self.pipes_in_loop:
            return True



        return False



class Problem1(SolverBase):
    def solve(self):
        maze = PipeMaze(self.input_data)
        print(maze.find_starting_pipe().offset_indices)
        route_indices = maze.traverse_pipes()
        print(len(route_indices) / 2)


class Problem2(SolverBase):
    def solve(self):
        maze = PipeMaze(self.input_data)
        maze.visit_non_pipe_tiles()


problem1 = Problem1("Input.txt")
problem1.solve()

test = Problem2("Part2TestInput.txt")
test.solve()
