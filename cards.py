from collections import namedtuple
import random


Card = namedtuple('Card', ['rank', 'suit'])


class CardsDeck:

    ranks = [str(x) for x in range(2, 11)] + list('JQKA')
    suits = ['spades', 'diamonds', 'clubs', 'hearts']

    def __init__(self):
        self._deck = [Card(rank, suit) for suit in self.suits
                                            for rank in self.ranks]

    def __len__(self):
        return len(self._deck)

    def __getitem__(self, index):
        return self._deck[index]

    def __setitem__(self, key, value):
        self._deck[key] = value

    def shuffle(self):
        random.shuffle(self._deck)

    def deal(self):
        return self._deck.pop(0)


class Player:

    def __init__(self, name):
        self._name = name
        self._cards = []

    @property
    def cards(self):
        return self._cards

    @property
    def name(self):
        return self._name

    def receive_card(self, card):
        self._cards.append(card)

    def return_cards(self):
        self._cards.clear()


class Table:

    def __init__(self, max_players=10):
        self._players = []
        self._cards = []
        self._deck = CardsDeck()
        self._max_players = max_players

    @property
    def players(self):
        return self._players

    @property
    def cards(self):
        return self._cards

    @property
    def deck(self):
        return self._deck

    @property
    def table_size(self):
        return self._max_players

    def receive_card(self, card):
        self._cards.append(card)

    def return_cards(self):
        self._cards.clear()

    def sit_player(self, player):
        if len(self._players) < self._max_players:
            self._players.append(player)
        else:
            raise IndexError('No more available seats. Maximum number of players reached.')

    def remove_player(self, player):
        self._players.remove(player)

    #def deal_card(self, player):
