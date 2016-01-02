import pytest
import poker


class TestPokerPlayer:

    def setup_class(self):
        self.player = poker.PokerPlayer('testPlayer')
        self.card = poker.Card('J', 'hearts')
        self.another_card = poker.Card('A', 'clubs')

    def test_player_no_chips(self):
        assert self.player.chips == 0

    def test_player_chips_exception(self):
        with pytest.raises(AttributeError):
            self.player.chips = 10

    def test_player_add_chips(self):
        assert self.player.add_chips(100) == 'Successfully added 100 chips'

    def test_player_add_exception(self):
        with pytest.raises(TypeError):
            self.player.add_chips(-10)

    def test_player_total_chips(self):
        assert self.player.chips == 100

    def test_player_bet(self):
        chips = self.player.chips
        self.player.bet(50)
        assert self.player.chips == (chips - 50)

    def test_player_bet_exception(self):
        with pytest.raises(TypeError):
            self.player.bet(-10)

    def test_player_bet_not_enough_chips(self):
        with pytest.raises(poker.NotEnoughChips):
            chips = self.player.chips + 1
            self.player.bet(chips)

    def test_player_receive_card(self):
        self.player.receive_card(self.card)
        self.player.receive_card(self.another_card)
        assert self.player.cards == [self.card, self.another_card]

    def test_player_fold(self):
        self.player.fold()
        assert not self.player.cards


class TestPokerTable:

    def setup(self):
        self.table = poker.PokerTable(max_players=3)
        self.player1 = poker.PokerPlayer('player1')
        self.player2 = poker.PokerPlayer('player2')
        self.player3 = poker.PokerPlayer('player3')
        self.player4 = poker.PokerPlayer('player4')

    def test_table_start_game_exception(self):
        self.table.sit_player(self.player1)
        with pytest.raises(poker.NotEnoughPlayers):
            self.table.start_game()

    def test_table_game_not_started(self):
        assert not self.table.game_started

    def test_table_start_game(self):
        self.table.sit_player(self.player1)
        self.table.sit_player(self.player2)
        assert self.table.start_game() == True
        assert self.table.game_started == True

    def test_table_deal_cards_exception(self):
        with pytest.raises(poker.GameNotStarted):
            self.table.deal_cards()

    def test_table_deal_cards(self):
        self.table.sit_player(self.player1)
        self.table.sit_player(self.player2)
        self.table.start_game()
        self.table.deal_cards()
        assert len(self.table.players[0].cards) == 2
        assert len(self.table.cards) == 5
        with pytest.raises(poker.TooManyCards):
            self.table.deal_cards()
        for player in self.table.players:
            player.return_cards()
        with pytest.raises(poker.TooManyCards):
            self.table.deal_cards()

