import functools

from SolverBase import SolverBase


class Mirror:

    def __init__(self, rows):
        self.rows = rows

    def find_horizontal_symmetrical_line(self):
        return self.find_vertical_symmetrical_line(list(zip(*self.rows)))

    def find_vertical_symmetrical_line(self, input_rows=None):
        rows = input_rows if input_rows is not None else self.rows
        row_len = len(rows[0])
        mid_point = int(row_len / 2)
        lookup_len = 2 * mid_point
        remainder = row_len % 2

        for counter in range(0, mid_point):
            left_mid = mid_point - counter - 1
            left_all_symmetrical = all([self.is_row_symmetrical(row[0:lookup_len - 2 * counter], left_mid) for row in rows])
            if left_all_symmetrical:
                return mid_point - counter

            right_mid = mid_point - counter - 1
            right_all_symmetrical = all([self.is_row_symmetrical(row[0 + remainder + 2 * counter:lookup_len + remainder], right_mid) for row in rows])
            if right_all_symmetrical:
               return mid_point + counter + remainder

        return 0

    @staticmethod
    @functools.cache
    def is_row_symmetrical(row, mid_index):
        zipped_row = zip(row[mid_index::-1], row[mid_index + 1:])
        return all([left == right for (left, right) in zipped_row])


class Problem1(SolverBase):

    def solve(self):
        result_vertical = 0
        result_horizontal = 0
        empty_indices = [-1] + self.find_empty_indices() + [len(self.input_data)]
        for index in range(len(empty_indices) - 1):
            mirror = Mirror(self.input_data[empty_indices[index]+1:empty_indices[index+1]])
            result_vertical += mirror.find_vertical_symmetrical_line()
            result_horizontal += mirror.find_horizontal_symmetrical_line() * 100

        print(result_vertical + result_horizontal)


solution = Problem1("Input.txt")
solution.solve()

