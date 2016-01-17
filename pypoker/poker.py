from pypoker.cards import CardsDeck, Player, Card, Table
from pypoker.evaluator import Hand, Evaluator



class NotEnoughChips(Exception):
    pass


class NotEnoughPlayers(Exception):
    pass


class GameNotStarted(Exception):
    pass


class TooManyCards(Exception):
    pass


class PokerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self._chips = 0

    @property
    def chips(self):
        return self._chips

    def add_chips(self, amount):
        if isinstance(amount, int) and amount > 0:
            self._chips += amount
            return 'Successfully added {} chips'.format(str(amount))
        else:
            raise TypeError('Only positive integers allowed.')

    def bet(self, amount):
        if isinstance(amount, int) and 0 < amount < self.chips:
            self._chips -= amount
            return amount
        elif amount > self.chips:
            raise NotEnoughChips('Total chips = {}'.format(self.chips))
        else:
            raise TypeError('Only positive integers allowed.')

    def fold(self):
        self.return_cards()


class PokerTable(Table):

    def __init__(self, max_players=10, min_players=2, cards_per_player=2,
                 cards_per_table=5):

        super().__init__(max_players)
        self.min_players = min_players
        self.cards_per_player = cards_per_player
        self.cards_per_table = cards_per_table
        self._game_started = False

    @property
    def game_started(self):
        return self._game_started

    def start_game(self):
        if len(self.players) >= self.min_players:
            self._game_started = True
            return self.game_started
        else:
            raise NotEnoughPlayers('Only {} players sit. Minimum of {} players '
                                   'required to start a game.'.format(len(
                                    self.players), self.min_players))

    def deal_cards(self):
        if not self.game_started:
            raise GameNotStarted()
        self._deck = CardsDeck()
        self.deck.shuffle()
        for n in range(self.cards_per_player):
            for player in self.players:
                if len(player.cards) >= self.cards_per_player:
                    raise TooManyCards
                card = self.deck.deal()
                player.receive_card(card)
        for i in range(self.cards_per_table):
            if len(self.cards) >= self.cards_per_table:
                    raise TooManyCards
            card = self.deck.deal()
            self.receive_card(card)

# class Game:


def test_play(num_players=2):
    table = PokerTable()
    players = [PokerPlayer(str(n)) for n in range(num_players)]
    #     PokerPlayer('p1'),
    #     PokerPlayer('p2'),
    #     PokerPlayer('p3'),
    #     PokerPlayer('p4'),
    #     PokerPlayer('p5')
    # ]

    values = {  800: 'Straight Flush',
                700: 'Four of a Kind',
                600: 'Full House',
                500: 'Flush',
                400: 'Straight',
                300: 'Three of Kind',
                200: 'Two Pair',
                100: 'One Pair',
                0:   'High Card'
                }

    for p in players:
        table.sit_player(p)
    table.start_game()
    table.deal_cards()
    #print('Board = {}'.format(table.cards))
    player_cards = [p.cards + table.cards for p in players]
    #for p in player:
    #    print('{} cards = {}'.format(p.name, p.cards))
    #for p in player_cards:
    #    print('cards: ', p)
    #print()
    hands = [Hand(cards) for cards in player_cards]
    best_hand = Evaluator.best_hand(hands)
    #print('Best Card: ', str(best_hand))
    ev =  Evaluator(best_hand[0]).hand_value()
    #print('Hand Value: ', values[ev.value])
    return values[ev.value]

if __name__ == '__main__':
    from collections import Counter
    import timeit
    results = []
    num_trials = 100000
    start_time = timeit.default_timer()
    for i in range(num_trials):
        results.append(test_play(5))
    counter = Counter(results)
    #print(counter)
    print(timeit.default_timer() - start_time)
    for k,v in counter.items():
        print(k, ' : ', 100 * v/num_trials, '%')





