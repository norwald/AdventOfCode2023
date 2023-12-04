from SolverBase import SolverBase
from queue import Queue


class Card:
    def __init__(self, string_raw):
        description = string_raw.strip().split("|")
        definition = description[0].strip().split(":")

        self.card_id = int(definition[0].strip().split()[1])
        self.winning_cards = set(definition[1].strip().split())
        self.card_hand = set(description[1].strip().split())

    def get_winning_cards_in_hand(self):
        return self.winning_cards.intersection(self.card_hand)


class RecursiveCardCrawler:

    def __init__(self, cards):
        self.cards = cards
        self.cards_to_visit = Queue()
        self.visited_cards = []

    def visit_all_cards(self):
        # reset counter in case of multiple calls
        self.visited_cards = []
        self.cards_to_visit = Queue()

        for card in self.cards:
            self.visit_card(card)

        while not self.cards_to_visit.empty():
            self.visit_card(self.cards_to_visit.get())

    def visit_card(self, card):
        self.visited_cards.append(card)
        next_card_index = card.card_id
        number_winning_cards = len(card.get_winning_cards_in_hand())

        if number_winning_cards > 0:
            for counter in range(next_card_index, next_card_index + number_winning_cards):
                if counter < len(self.cards):
                    self.cards_to_visit.put(self.cards[counter])


class Problem1(SolverBase):

    def solve(self):
        num_winning_cards = [len(Card(line).get_winning_cards_in_hand()) for line in self.input_data]
        print(sum([2 ** (num - 1) for num in num_winning_cards if num > 0]))


class Problem2(SolverBase):

    def solve(self):
        cards = [Card(line) for line in self.input_data]
        cards_crawler = RecursiveCardCrawler(cards)
        cards_crawler.visit_all_cards()

        print(len(cards_crawler.visited_cards))


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
