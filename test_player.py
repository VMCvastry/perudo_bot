import unittest

from perudo_game.game.game_info import GameInfo
from perudo_game.game.player_entity import PlayerEntity
from perudo_game.players import PlayerInterface
from perudo_game.players.playerTest import BotTest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.player: PlayerInterface = BotTest(257)
        self.player.set_rolled_dices([5, 5, 4, 4, 4, 3])
        self.players = [PlayerEntity(BotTest(0), 0), PlayerEntity(BotTest(1), 1)]

    def test_is_player_instance(self):
        self.assertIsInstance(self.player, PlayerInterface)

    def test_name_not_null(self):
        self.assertIsNotNone(self.player.get_player_name())

    def test_set_numbers(self):
        self.assertIsNone(self.player.set_rolled_dices([1, 2, 3]))

    def test_not_none_on_start(self):
        info = GameInfo(self.players, 0, [[]], True)
        self.assertIsNotNone(self.player.make_a_move(info))

    # def test_grater_than_last(self):
    #     info = GameInfo(self.players, 0, [[3,5]], True)
    #     move=self.player.make_a_move(info)
    #     condition=move is None or
    #     self.assertTrue()


if __name__ == "__main__":
    unittest.main()
