from SolverBase import SolverBase


class NumberSequence:
    def __init__(self, string_raw):
        self.number_sequence = [int(num) for num in string_raw.strip().split()]

    def interpolate_next_number(self):
        all_differences = self.find_difference_in_sequence()
        for counter in range(len(all_differences) - 2, -1, -1):
            last_number_current = all_differences[counter][-1]
            last_number_prev = all_differences[counter + 1][-1]
            all_differences[counter].append(last_number_prev + last_number_current)

        return self.number_sequence[-1] + all_differences[0][-1]

    def interpolate_prev_number(self):
        all_differences = self.find_difference_in_sequence()
        for counter in range(len(all_differences) - 2, -1, -1):
            first_number_current = all_differences[counter][0]
            first_number_prev = all_differences[counter + 1][0]
            all_differences[counter] = [first_number_current - first_number_prev] + all_differences[counter]

        return self.number_sequence[0] - all_differences[0][0]

    def find_difference_in_sequence(self):
        difference = self.find_difference(self.number_sequence)
        all_differences = [difference]
        while not self.all_zeroes(difference):
            difference = self.find_difference(difference)
            all_differences.append(difference)

        return all_differences

    @staticmethod
    def find_difference(sequence):
        result = []
        for counter in range(0, len(sequence) - 1):
            result.append(sequence[counter + 1] - sequence[counter])
        return result

    @staticmethod
    def all_zeroes(sequence):
        return all(num == 0 for num in sequence)


class Problem1(SolverBase):

    def solve(self):
        sequences = [NumberSequence(line) for line in self.input_data]
        forecasts = [sequence.interpolate_next_number() for sequence in sequences]
        print(sum(forecasts))


class Problem2(SolverBase):

    def solve(self):
        sequences = [NumberSequence(line) for line in self.input_data]
        forecasts = [sequence.interpolate_prev_number() for sequence in sequences]
        print(sum(forecasts))


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
