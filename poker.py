from cards import Card, CardsDeck, Player, Table


class PokerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.chips = 0