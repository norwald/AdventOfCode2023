from SolverBase import SolverBase


class Card:
    def __init__(self, string_raw):
        description = string_raw.strip().split("|")
        definition = description[0].strip().split(":")

        self.card_id = definition[0].strip().split()[1]
        self.winning_cards = set(definition[1].strip().split())
        self.card_hand = set(description[1].strip().split())

    def get_winning_cards_in_hand(self):
        return self.winning_cards.intersection(self.card_hand)


class Problem1(SolverBase):

    def solve(self):
        num_winning_cards = [len(Card(line).get_winning_cards_in_hand()) for line in self.input_data]
        print(sum([2 ** (num - 1) for num in num_winning_cards if num > 0]))


problem1 = Problem1("Input.txt")
problem1.solve()
