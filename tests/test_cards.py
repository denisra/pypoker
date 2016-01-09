import pytest
import cards


class TestCardsDeck:

    def setup_class(self):
        self.deck = cards.CardsDeck()

    def test_len(self):
        assert len(self.deck) == 52

    def test_getitem(self):
        assert self.deck[0] == cards.Card(rank='2', suit='spades')

    def test_getitem_index_exception(self):
        with pytest.raises(IndexError):
            self.deck[85]

    def test_getitem_type_exception(self):
        with pytest.raises(TypeError):
            self.deck['abc']

    def test_shuffle(self):
        old_deck = self.deck._deck[:]
        self.deck.shuffle()
        assert self.deck._deck != old_deck

    def test_deal(self):
        card = self.deck.deal()
        assert isinstance(card, cards.Card)

    def test_deal_len(self):
        self.deck.deal()
        assert len(self.deck) < 52

    def test_str(self):
        assert str(self.deck)


class TestPlayer:

    def setup_class(self):
        self.player = cards.Player('testPlayer')
        self.card = cards.Card('11', 'hearts')
        self.another_card = cards.Card('14', 'clubs')

    def test_player_name(self):
        assert self.player.name == 'testPlayer'

    def test_name_exception(self):
        with pytest.raises(AttributeError):
            self.player.name = 'testPlayer2'

    def test_empty_cards(self):
        assert not self.player.cards

    def test_cards_exception(self):
        with pytest.raises(AttributeError):
            self.player.cards = [1, 2]

    def test_receive_card(self):
        self.player.receive_card(self.card)
        assert self.player.cards[0] == self.card

    def test_receive_another_card(self):
        self.player.receive_card(self.another_card)
        assert self.player.cards[1] == self.another_card

    def test_return_cards(self):
        self.player.return_cards()
        assert not self.player.cards

class TestTable:

    def setup_class(self):
        self.table = cards.Table(max_players=3)
        self.card = self.table.deck[0]
        self.another_card = self.table.deck[1]
        self.player1 = cards.Player('testPlayer1')
        self.player2 = cards.Player('testPlayer2')
        self.player3 = cards.Player('testPlayer3')
        self.other_player = cards.Player('otherPlayer')
        self.players = [self.player1, self.player2, self.player3]

    def test_empty_cards(self):
        assert not self.table.cards

    def test_cards_exception(self):
        with pytest.raises(AttributeError):
            self.table.cards = [1, 2]

    def test_receive_card(self):
        self.table.receive_card(self.card)
        assert self.table.cards[0] == self.card

    def test_receive_another_card(self):
        self.table.receive_card(self.another_card)
        assert self.table.cards[1] == self.another_card

    def test_return_cards(self):
        self.table.return_cards()
        assert not self.table.cards

    def test_deck_exception(self):
        with pytest.raises(AttributeError):
            self.table.deck = [1, 2]

    def test_deck_deal(self):
        assert self.table.deck.deal()

    def test_table_size_exception(self):
        with pytest.raises(AttributeError):
            self.table.table_size = 5

    def test_table_size(self):
        assert self.table.table_size == 3

#    def test_deck_shuffle(self):
#        assert self.table.deck.shuffle() == None

    def test_no_players(self):
        assert not self.table.players

    def test_players_exception(self):
        with pytest.raises(AttributeError):
            self.table.players = self.players

    def test_sit_player(self):
        self.table.sit_player(self.player1)
        self.table.sit_player(self.player2)
        self.table.sit_player(self.player3)
        assert self.table.players == self.players

    def test_sit_player_again_exception(self):
        with pytest.raises(AttributeError):
            self.table.sit_player(self.player1)

    def test_max_players(self):
        with pytest.raises(IndexError):
            self.table.sit_player(self.other_player)

    def test_player_leave(self):
        self.table.remove_player(self.player1)
        assert self.table.players == [self.player2, self.player3]

    def test_other_player_leave(self):
        with pytest.raises(ValueError):
            self.table.remove_player(self.other_player)