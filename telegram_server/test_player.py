import random, json
import unittest
from copy import deepcopy

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from perudo_game.game.player_entity import PlayerEntity
from perudo_game.players import PlayerInterface
from perudo_game.players.playerTest import BotTest


def is_valid_move(info: GameInfo, move: GameMove):  # todo raise error in Game_Core
    last = info.moves_history[-1][-1]
    return move.amount > last.amount or (
        move.amount == last.amount and move.number > last.number
    )


def is_valid_json(encoded):
    try:
        json.loads(encoded)
    except ValueError as e:
        return False
    return True


def generate_random_history(n_players):  # TODO real history generator
    return [[GameMove(1, 3)]]


def generate_random_status():
    n_players = random.randint(2, 5)
    players_info = [
        (random.randint(0, 50), random.randint(0, 6)) for _ in range(n_players)
    ]
    return GameInfo(
        players_info, random.randint(0, 100), generate_random_history(n_players), False
    )


def generate_random_status_first_move():
    n_players = random.randint(2, 5)
    players_info = [
        (random.randint(0, 50), random.randint(0, 6)) for _ in range(n_players)
    ]
    history = generate_random_history(n_players)
    history.append([])
    return GameInfo(players_info, random.randint(0, 100), history, True)


def generate_numbers():
    n_dices = random.randint(1, 6)
    return [random.randint(1, 6) for _ in range(n_dices)]


def test_not_none_on_start():
    info = generate_random_status_first_move()
    player = BotTest("{}")
    move, status = player.make_a_move(deepcopy(info), generate_numbers())
    return (
        isinstance(move, GameMove) and isinstance(status, str) and is_valid_json(status)
    )


def test_valid_move():
    info = generate_random_status()
    player = BotTest("{}")
    move, status = player.make_a_move(deepcopy(info), generate_numbers())
    return (
        (isinstance(move, GameMove) and is_valid_move(info, move) or move is None)
        and isinstance(status, str)
        and is_valid_json(status)
    )


class MyTestCase(unittest.TestCase):
    n_tests = 100
    # def setUp(self):
    #     self.player: PlayerInterface = BotTest("{}")
    #     self.players = [PlayerEntity(BotTest, 0), PlayerEntity(BotTest, 1)]

    def test_is_player_instance(self):
        self.assertIsInstance(BotTest("{}"), PlayerInterface)

    def test_name_not_null(self):
        self.assertIsInstance(BotTest.get_player_name(), str)

    def test_not_none_on_start(self):
        valid = True
        for _ in range(self.n_tests):
            valid = valid and test_not_none_on_start()
        self.assertTrue(valid)

    def test_valid_move(self):
        valid = True
        for _ in range(self.n_tests):
            valid = valid and test_valid_move()
        self.assertTrue(valid)


if __name__ == "__main__":
    unittest.main()
