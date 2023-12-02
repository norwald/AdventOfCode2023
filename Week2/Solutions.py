from SolverBase import SolverBase


class Game:
    def __init__(self, line):
        description = line.split(":")
        self.id = int(description[0].split(" ")[1])
        self.draws = [Draw(draw) for draw in description[1].split(";")]

    def is_valid_game(self, allowed_color_count):
        return all(draw.is_valid_draw(allowed_color_count) for draw in self.draws)

    def find_min_valid_color_count(self):
        min_valid_color_count = {"red": 0, "blue": 0, "green": 0}

        for draw in self.draws:
            for subset in draw.subsets:
                if subset.count > min_valid_color_count[subset.color]:
                    min_valid_color_count[subset.color] = subset.count

        return min_valid_color_count


class Draw:
    def __init__(self, raw_string):
        raw_string_split = raw_string.strip().split(",")
        self.subsets = [Subset(subset) for subset in raw_string_split]

    def is_valid_draw(self, allowed_color_count):
        return all(subset.count <= allowed_color_count[subset.color] for subset in self.subsets)


class Subset:
    def __init__(self, raw_string):
        raw_string_split = raw_string.strip().split(" ")
        self.color = raw_string_split[1]
        self.count = int(raw_string_split[0])


class Week2Problem1(SolverBase):

    def __init__(self, content, allowed_color_count):
        super().__init__(content)
        self.allowed_color_count = allowed_color_count

    def solve(self):
        games = list(map(lambda line: Game(line), self.content))
        valid_games = [game.id for game in games if game.is_valid_game(self.allowed_color_count)]
        print(sum(valid_games))


class Week2Problem2(SolverBase):
    def solve(self):
        games = list(map(lambda line: Game(line), self.content))
        min_valid_color_counts = [game.find_min_valid_color_count() for game in games]
        valid_games_cube = [valid_game["red"] * valid_game["blue"] * valid_game["green"] for valid_game in
                            min_valid_color_counts]

        print(sum(valid_games_cube))


problem1 = Week2Problem1("Input.txt", {"red": 12, "green": 13, "blue": 14})
problem1.solve()

problem2 = Week2Problem2("Input.txt")
problem2.solve()
