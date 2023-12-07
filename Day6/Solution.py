from functools import reduce

from SolverBase import SolverBase


class Race:
    def __init__(self, lines, number_parser=lambda string_raw: [int(num) for num in string_raw.strip().split()]):
        self.times = number_parser(lines[0].strip().split(":")[1])
        self.distances = number_parser(lines[1].strip().split(":")[1])
        self.races = list(zip(self.times, self.distances))

    def get_num_wins_all_races(self):
        return [Race.get_num_wins(time, distance) for (time, distance) in self.races]

    @staticmethod
    def get_num_wins(time, distance):
        num_wins = 0
        max_parabola = int((time + 1) / 2)

        left_offset = 0
        while max_parabola <= time:
            distance_traveled = (time - max_parabola) * max_parabola

            max_parabola_left = max_parabola - left_offset
            distance_traveled_left = (time - max_parabola_left) * max_parabola_left

            if distance_traveled > distance:
                num_wins += 1

            if max_parabola_left != max_parabola and distance_traveled_left > distance:
                num_wins += 1

            if distance_traveled >= distance or distance_traveled_left >= distance:
                max_parabola += 1
                left_offset += 2
            else:
                break

        return num_wins


class Problem1(SolverBase):

    def solve(self):
        race = Race(self.input_data)
        num_wins = race.get_num_wins_all_races()
        print(reduce(lambda x, y: x * y, num_wins, 1))


class Problem2(SolverBase):

    def solve(self):
        race = Race(self.input_data, lambda string_raw: [int(''.join(string_raw.split()))])
        num_wins = race.get_num_wins_all_races()
        print(reduce(lambda x, y: x * y, num_wins, 1))


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
