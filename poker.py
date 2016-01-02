from cards import Card, CardsDeck, Player, Table


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

#class Game: