from enum import Enum

from SolverBase import SolverBase


class Hand(Enum):
    FIVE_KIND = 8
    FOUR_KIND = 7
    FULL_HOUSE = 6
    THREE_KIND = 5
    TWO_PAIR = 4
    PAIR = 3
    HIGH_CARD = 2


class Bet:
    card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,
                   '2': 2}

    card_values_joker = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
                         '3': 3,
                         '2': 2}

    def __init__(self, string_raw, joker_plays=False):
        split_string = string_raw.strip().split()

        self.cards = split_string[0]
        self.bet_amount = int(split_string[1])
        self.cards_in_hand = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, 'T': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0,
                              '3': 0,
                              '2': 0}
        self.hand = Hand.HIGH_CARD
        self.order_value = -1
        self.card_values_lookup = Bet.card_values_joker if joker_plays else Bet.card_values
        self.joker_plays = joker_plays

        self.populate_cards_in_hand()
        self.eval_hand()
        self.set_order_value()

    def populate_cards_in_hand(self):
        for card in self.cards:
            self.cards_in_hand[card] += 1

    def eval_hand(self):
        card_counts = self.get_hands_with_joker() if self.joker_plays else self.cards_in_hand.values()
        if any(count == 5 for count in card_counts):
            self.hand = Hand.FIVE_KIND
        elif any(count == 4 for count in card_counts):
            self.hand = Hand.FOUR_KIND
        elif any(count == 3 for count in card_counts) and any(count == 2 for count in card_counts):
            self.hand = Hand.FULL_HOUSE
        elif any(count == 3 for count in card_counts):
            self.hand = Hand.THREE_KIND
        elif len([pair for pair in card_counts if pair == 2]) == 2:
            self.hand = Hand.TWO_PAIR
        elif any(count == 2 for count in card_counts):
            self.hand = Hand.PAIR

    def get_hands_with_joker(self):
        num_jokers = self.cards_in_hand['J']
        cards_count = [entry[1] for entry in sorted(self.cards_in_hand.items(), key=lambda item: item[1], reverse=True)
                       if entry[0] != 'J']
        cards_count[0] += num_jokers

        return cards_count

    def set_order_value(self):
        self.order_value = self.hand.value * 10000000000 + self.card_values_lookup[self.cards[0]] * 100000000 + \
                           self.card_values_lookup[self.cards[1]] * 1000000 + self.card_values_lookup[
                               self.cards[2]] * 10000 + \
                           self.card_values_lookup[self.cards[3]] * 100 + \
                           self.card_values_lookup[self.cards[4]]
    # A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2


class Problem1(SolverBase):

    def solve(self):
        bets = [Bet(bet_string) for bet_string in self.input_data]
        bets.sort(key=lambda bet: bet.order_value)

        score = 0
        for counter in range(0, len(bets)):
            score += (counter + 1) * bets[counter].bet_amount

        print(score)


class Problem2(SolverBase):

    def solve(self):
        bets = [Bet(bet_string, True) for bet_string in self.input_data]
        bets.sort(key=lambda bet: bet.order_value)

        score = 0
        for counter in range(0, len(bets)):
            score += (counter + 1) * bets[counter].bet_amount

        print(score)


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
