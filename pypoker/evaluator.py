"""
Poker Hand Evaluator module.
Most of the logic was borrowed from Professor's Peter Norvig CS212 course.
"""


from collections import namedtuple, Counter

HandValue = namedtuple('HandValue', ['value', 'hand', 'ranks'])


class Hand:

    """Poker Hand class

     A = 14
     K = 13
     Q = 12
     J = 11
     T = 10
    """

    def __init__(self, cards):
        self.cards = cards
        self.ranks = self.convert_ranks()
        self.suits = [card.suit for card in cards]

    def convert_ranks(self):
        ranks = ['--23456789TJQKA'.index(card.rank) for card in self.cards]
        ranks.sort(reverse=True)
        return ranks if ranks != [14, 5, 4, 3, 2] else [5, 4, 3, 2, 1]

    def __str__(self):
        return str([[card.rank, card.suit] for card in self.cards])

    __repr__ = __str__


class Evaluator:

    """ Evaluates a given Hand object and returns a HandValue namedtuple
    based on the following table:

    :returns:

    Royal Flush:    HandValue(900, None, None)
    Straight Flush: HandValue(800, None, None)
    Four of a Kind: HandValue(700, [self.kind(4), self.kind(1)], None)
    Full House:     HandValue(600, [self.kind(3), self.kind(2)], None)
    Flush:          HandValue(500, None, ranks)
    Straight:       HandValue(400. None, ranks)
    Three of Kind:  HandValue(300, [self.kind(3)], None)
    Two Pair:       HandValue(200, [self.two_pair()], ranks)
    One Pair:       HandValue(100, [self.kind(2)], ranks)
    High Card:      HandValue(0, None, ranks)

    """

    def __init__(self, hand):
        self.hand = hand
        # self.value = self.hand_value()

    def _ranks_set(self):
        return sorted(list(set(self.hand.ranks)), reverse=True)

    def straight_flush(self):
        """
        :return: True if flush and straight == True
        """
        if not self.flush() or not self.straight():
            return False
        all_suits = Counter(self.hand.suits)
        suit = [k for k,v in all_suits.items() if v == max(all_suits.values())][0]
        cards = [card for card in self.hand.cards if card.suit == suit]
        hand = Hand(cards)
        max_ = max(hand.ranks)
        min_ = min(hand.ranks)
        return (len(hand.ranks) == 5 and (max_ - min_) == 4) or (len(
            hand.ranks) == 6 and (max_ - min_) == 5) or (len(hand.ranks) == 7
                                                         and (max_ - min_) == 6)


    def straight(self):
        """
        :return: True if the highest card minus the lowest card == 4
        """
        ranks = self._ranks_set()
        max_ = max(ranks)
        min_ = min(ranks)
        return (len(ranks) == 5 and (max_ - min_) == 4) or (len(ranks) == 6
            and (max_ - min_) == 5) or (len(ranks) == 7 and (max_ - min_) == 6)

    def flush(self):
        """
        :return: True if all suits are the same
        """
        suits = Counter(self.hand.suits)
        return (5 in suits.values()) or (6 in suits.values()) or (7 in suits.values())


    def two_pair(self):
        """
        :return: (highest, lowest) pair
        """
        result = [r for r in set(self.hand.ranks) if self.hand.ranks.count(r) == 2]
        return (max(result), min(result)) if len(result) == 2 else None

    def kind(self, n):
        """
        :return: the rank if its count == n
        """
        for rank in set(self.hand.ranks):
            if self.hand.ranks.count(rank) == n:
                return rank
        return None

    def hand_value(self):
        if self.straight_flush():
            return HandValue(800, None, self.hand.ranks)
        elif self.kind(4):
            return HandValue(700, [self.kind(4)], self.hand.ranks)
        elif self.kind(3) and self.kind(2):
            return HandValue(600, [self.kind(3), self.kind(2)], None)
        elif self.flush():
            return HandValue(500, None, self.hand.ranks)
        elif self.straight():
            return HandValue(400, None, self.hand.ranks)
        elif self.kind(3):
            return HandValue(300, [self.kind(3)], None)
        elif self.two_pair():
            return HandValue(200, list(self.two_pair()), self.hand.ranks)
        elif self.kind(2):
            return HandValue(100, [self.kind(2)], self.hand.ranks)
        else:
            return HandValue(0, None, self.hand.ranks)

    def __gt__(self, other):
        hand_value = self.hand_value()
        other_value = other.hand_value()
        if hand_value.value != other_value.value:
            return hand_value.value > other_value.value
        if hand_value.hand != other_value.hand:
            try:
                return hand_value.hand > other_value.hand
            except TypeError:
                print('hand_value: ', hand_value)
                print('other_value: ', other_value)
        if hand_value.ranks != other_value.ranks:
            return hand_value.ranks > other_value.ranks
        return False

    def __eq__(self, other):
        if self.hand == other.hand or self.hand_value() == other.hand_value():
            return True
        else:
            return False

    @classmethod
    def best_hand(cls, hands):
        best_hand_ = []
        for hand in hands:
            hand_value = cls(hand)
            if not best_hand_ or hand_value > cls(best_hand_[0]):
                best_hand_ = [hand]
            elif hand_value == cls(best_hand_[0]):
                best_hand_.append(hand)
        return best_hand_
