import functools

from SolverBase import SolverBase


class Mirror:

    def __init__(self, rows):
        self.rows = rows

    def find_horizontal_symmetrical_line(self):
        col_len = len(self.rows)
        mid_point = int(col_len / 2)
        lookup_len = 2 * mid_point
        remainder = col_len % 2

        for counter in range(0, mid_point):
            up_mid = mid_point - counter - 1
            up_all_symmetrical = self.are_rows_symmetrical(tuple(self.rows[0:lookup_len - 2 * counter]), up_mid)
            if up_all_symmetrical:
                return mid_point - counter

            down_mid = mid_point - counter - 1
            down_all_symmetrical = self.are_rows_symmetrical(tuple(self.rows[0 + remainder + 2 * counter:lookup_len + remainder]), down_mid)
            if down_all_symmetrical:
                return mid_point + counter + remainder

        return -1

    @staticmethod
    @functools.cache
    def are_rows_symmetrical(rows, mid_index):
        print(rows)
        print(rows[mid_index::-1])
        print(rows[mid_index + 1:])
        zipped_rows = zip(rows[mid_index::-1], rows[mid_index + 1:])
       # print(list(zipped_rows))
        return all([up == down for (up, down) in zipped_rows])

    def find_vertical_symmetrical_line(self):
        row_len = len(self.rows[0])
        mid_point = int(row_len / 2)
        lookup_len = 2 * mid_point
        remainder = row_len % 2

        for counter in range(0, mid_point):
            left_mid = mid_point - counter - 1
            left_all_symmetrical = all([self.is_row_symmetrical(row[0:lookup_len - 2 * counter], left_mid) for row in self.rows])
            if left_all_symmetrical:
                return mid_point - counter

            right_mid = mid_point - counter - 1
            right_all_symmetrical = all([self.is_row_symmetrical(row[0 + remainder + 2 * counter:lookup_len + remainder], right_mid) for row in self.rows])
            if right_all_symmetrical:
               return mid_point + counter + remainder

        return -1

    @staticmethod
    @functools.cache
    def is_row_symmetrical(row, mid_index):
        print(row[mid_index::-1])
        print(row[mid_index + 1:])
        zipped_row = zip(row[mid_index::-1], row[mid_index + 1:])
        return all([left == right for (left, right) in zipped_row])


class Problem1(SolverBase):

    def solve(self):
        result_vertical = 0
        result_horizontal = 0
        empty_indices = [-1] + self.find_empty_indices() + [len(self.input_data)]
        for index in range(len(empty_indices) - 1):
            mirror = Mirror(self.input_data[empty_indices[index]+1:empty_indices[index+1]])

            vertical_line = mirror.find_vertical_symmetrical_line()
            horizontal_line = mirror.find_horizontal_symmetrical_line()

            if vertical_line != -1:
                result_vertical += vertical_line
            if horizontal_line != -1:
                result_horizontal += horizontal_line * 100

        print(result_vertical + result_horizontal)


solution = Problem1("Input.txt")
solution.solve()
