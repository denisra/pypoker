from pypoker.cards import *
from pypoker.evaluator import *


class TestSetup:

    def setup(self):
        self.deck = CardsDeck()
        self.royal_flush = Hand(self.deck[8:13]) # [TS, JS, QS, KS, AS]
        self.straight_flush = Hand(self.deck[5:10]) # [7S, 8S, 9S, TS, JS]
        self.four_of_kind = Hand(self.deck[0:52:13] + [self.deck[1]]) # [2S, 2D, 2C, 2H, 3S]
        self.full_house = Hand(self.deck[0:39:13] + self.deck[11:26:13]) #[2S, 2D, 2C, KS, KD]
        self.flush = Hand(self.deck[3:12:2]) # [5S, 7S, 9S, JS, KS]
        self.straight = Hand(self.deck[:3] + self.deck[16:18]) # [2S, 3S, 4S, 5D, 6D]
        self.low_straight = Hand([Card('A', 'diamonds')] + self.deck[:4]) #[AD, 2S, 3S, 4S, 5S])
        self.three_of_kind = Hand(self.deck[0:39:13] + self.deck[1:3]) #[2S, 2D, 2C, 3S, 4S]
        self.two_pair = Hand(self.deck[0:26:13] + self.deck[11:26:13] + [self.deck[5]]) #[2S, 2D, KS, KD, 7S]
        self.pair = Hand(self.deck[3:12:3] + self.deck[11:25:13]) # [5S, 8S, JS, KS, KD]
        self.high_card = Hand(self.deck[9:18:2]) # [JS, KS, 2D, 4D, 6D]
        self.high_card_A = Hand(self.deck[9:26:4]) # [JS, 2D, 6D, TD, AD]


class TestHand(TestSetup):

    def test_hand(self):
        ranks1 = sorted([int(rank) for rank, suit in self.deck[:5]], reverse=True)
        suits1 = len(set([suit for rank, suit in self.deck[:5]]))
        assert ranks1 == self.straight.ranks
        #assert suits1 == len(set(self.straight.suits))
        ranks2 = sorted([int(rank) if rank != 'A' else 1 for rank, suit in [
            Card('A', 'diamonds')] + self.deck[:4]], reverse=True)
        suits2 = len(set([suit for rank, suit in [Card('A', 'diamonds')] + self.deck[:4]]))
        assert ranks2 == self.low_straight.ranks
        assert suits2 == len(set(self.low_straight.suits))


class TestEvaluator(TestSetup):

    def test_evaluator(self):
        ev_royal_flush = Evaluator(self.royal_flush)
        assert ev_royal_flush.royal_flush()
        ev_straight = Evaluator(self.straight)
        assert ev_straight.straight()
        assert not ev_straight.flush()
        assert not ev_straight.royal_flush()
        ev_low_straight = Evaluator(self.low_straight)
        assert ev_low_straight.straight()
        assert ev_low_straight.flush() == False
        ev_two_pair = Evaluator(self.two_pair)
        assert ev_two_pair.two_pair()
        ev_straight_flush = Evaluator(self.straight_flush)
        assert ev_straight_flush.straight() and ev_straight_flush.flush()
        ev_four_of_kind = Evaluator(self.four_of_kind)
        assert ev_four_of_kind.kind(4)
        assert not ev_four_of_kind.kind(2)
        ev_full_house = Evaluator(self.full_house)
        assert ev_full_house.kind(3) and ev_full_house.kind(2)
        ev_flush = Evaluator(self.flush)
        assert ev_flush.flush()
        ev_three_of_kind = Evaluator(self.three_of_kind)
        assert ev_three_of_kind.kind(3)
        ev_pair = Evaluator(self.pair)
        assert ev_pair.kind(2)
        ev_high_card = Evaluator(self.high_card)
        #assert ev_high_card.

        ###### Evaluate hand_value method #####
        assert ev_royal_flush.hand_value() == HandValue(900, None, None)
        assert ev_straight_flush.hand_value() == HandValue(800, None, None)
        assert ev_four_of_kind.hand_value() == HandValue(700, [2, 3], None)
        assert ev_full_house.hand_value() == HandValue(600, [2, 13], None)
        assert ev_flush.hand_value() == HandValue(500, None, self.flush.ranks)
        assert ev_straight.hand_value() == HandValue(400, None, self.straight.ranks)
        assert ev_three_of_kind.hand_value() == HandValue(300, [2], None)
        assert ev_two_pair.hand_value() == HandValue(200, [13, 2], self.two_pair.ranks)
        assert ev_pair.hand_value() == HandValue(100, [13], self.pair.ranks)
        assert ev_high_card.hand_value() == HandValue(0, None, self.high_card.ranks)


        ##### __gt__ method ####
        assert ev_royal_flush > ev_straight_flush
        assert not ev_straight_flush > ev_royal_flush
        assert ev_straight_flush < ev_royal_flush
        assert ev_straight > ev_low_straight
        assert ev_low_straight < ev_straight
        assert not ev_straight > ev_straight

        #### best_hand method ####
        assert Evaluator.best_hand([self.royal_flush, self.straight]) == [self.royal_flush]
        assert Evaluator.best_hand([self.royal_flush, self.royal_flush]) == [self.royal_flush, self.royal_flush]
        assert Evaluator.best_hand([self.low_straight, self.straight]) == [self.straight]
        assert Evaluator.best_hand([self.flush, self.full_house, self.pair]) == [self.full_house]
        assert Evaluator.best_hand([self.high_card, self.high_card_A]) == [self.high_card_A]
        assert Evaluator.best_hand([self.high_card_A, self.three_of_kind]) == [self.three_of_kind]


