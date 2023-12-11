import math

from SolverBase import SolverBase


class Galaxy:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Universe:

    def __init__(self, input_lines=None):
        self.universe = self.__expand_universe(input_lines) if input_lines is not None else []
        self.galaxies = self.find_galaxies() if input_lines is not None else []

    def __expand_universe(self, input_lines):
        expanded = input_lines.copy()
        empty_line = "." * len(input_lines[0])
        empty_lines_counter = 0
        for row_counter in range(0, len(input_lines)):
            if self.are_all_cols_empty(expanded[row_counter + empty_lines_counter]):
                expanded = expanded[0:  row_counter + empty_lines_counter] + [empty_line] + expanded[
                                                                                            row_counter + empty_lines_counter: len(
                                                                                                expanded)]
                empty_lines_counter += 1

        empty_col_counter = 0
        for col_counter in range(0, len(empty_line)):
            if self.are_all_rows_empty(expanded, col_counter + empty_col_counter):
                self.__add_empty_colum(expanded, col_counter + empty_col_counter)
                empty_col_counter += 1

        return expanded

    @staticmethod
    def are_all_cols_empty(row):
        return all(character != "#" for character in row)

    @staticmethod
    def are_all_rows_empty(universe, col_index):
        for row in universe:
            if row[col_index] == "#":
                return False

        return True

    @staticmethod
    def __add_empty_colum(universe, col_index):
        for counter in range(0, len(universe)):
            universe[counter] = universe[counter][0:col_index] + "." + universe[counter][
                                                                       col_index:len(universe[counter])]

    def find_galaxies(self):
        galaxies = []
        for row_counter in range(0, len(self.universe)):
            for col_counter in range(0, len(self.universe[0])):
                if self.universe[row_counter][col_counter] == "#":
                    galaxies.append(Galaxy(row_counter, col_counter))

        return galaxies

    def find_shortest_distances(self):
        combinations = self.generate_galaxy_pairs()
        return [math.fabs(pair[1].row - pair[0].row) + math.fabs(pair[1].column - pair[0].column) for pair in
                combinations]

    def generate_galaxy_pairs(self):
        combinations = []
        for first in range(0, len(self.galaxies)):
            for second in range(first + 1, len(self.galaxies)):
                combinations.append((self.galaxies[first], self.galaxies[second]))
        return combinations


class SmartUniverse(Universe):
    def __init__(self, input_lines, expansion_addon):
        super().__init__()
        self.universe = input_lines
        self.galaxies = super().find_galaxies()
        self.expansion_addon = expansion_addon
        self.__init_addons()

    def __init_addons(self):
        self.empty_rows_addon = []
        for row in self.universe:
            if super().are_all_cols_empty(row):
                self.empty_rows_addon.append(self.expansion_addon)
            else:
                self.empty_rows_addon.append(0)

        self.empty_cols_addon = []
        for col_counter in range(0, len(self.universe[0])):
            if super().are_all_rows_empty(self.universe, col_counter):
                self.empty_cols_addon.append(self.expansion_addon)
            else:
                self.empty_cols_addon.append(0)

    def find_shortest_distances(self):
        shortest_distances = []
        combinations = super().generate_galaxy_pairs()

        for pair in combinations:
            start_row = min(pair[0].row, pair[1].row)
            end_row = max(pair[0].row, pair[1].row)
            rows_addon = sum(self.empty_rows_addon[start_row:end_row])
            dist_rows = end_row - start_row + rows_addon

            start_col = min(pair[0].column, pair[1].column)
            end_col = max(pair[0].column, pair[1].column)
            cols_addon = sum(self.empty_cols_addon[start_col:end_col])
            dist_cols = end_col - start_col + cols_addon
            shortest_distances.append(dist_rows + dist_cols)

        return shortest_distances


class Problem1(SolverBase):

    def solve(self):
        universe = Universe(self.input_data)
        shortest_distances = universe.find_shortest_distances()
        print(sum(shortest_distances))


class Problem2(SolverBase):

    def solve(self):
        universe = SmartUniverse(self.input_data, 999999)
        shortest_distances = universe.find_shortest_distances()
        print(sum(shortest_distances))


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
