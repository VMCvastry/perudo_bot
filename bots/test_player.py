import random, json
import traceback
import unittest
from copy import deepcopy

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class TestNotPassedException(Exception):
    def __init__(self, message):
        super().__init__(message)


def is_valid_move(info: GameInfo, move: GameMove):
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


def test_not_none_on_start(bot: type[PlayerInterface]):
    info = generate_random_status_first_move()
    player = bot("{}")
    move, status = player.make_a_move(deepcopy(info), generate_numbers())
    return (
        isinstance(move, GameMove) and isinstance(status, str) and is_valid_json(status)
    )


def test_valid_move(bot: type[PlayerInterface]):
    info = generate_random_status()
    player = bot("{}")
    move, status = player.make_a_move(deepcopy(info), generate_numbers())
    return (
        (isinstance(move, GameMove) and is_valid_move(info, move) or move is None)
        and isinstance(status, str)
        and is_valid_json(status)
    )


class TestBot:
    n_tests = 100

    def __init__(self, bot: type[PlayerInterface]):
        self.bot = bot

    def test_is_player_instance(self):
        return isinstance(self.bot("{}"), PlayerInterface)

    def test_name_not_null(self):
        return isinstance(self.bot.get_player_name(), str)

    def test_not_none_on_start(self):
        valid = True
        for _ in range(self.n_tests):
            valid = valid and test_not_none_on_start(self.bot)
        return valid

    def test_valid_move(self):
        valid = True
        for _ in range(self.n_tests):
            valid = valid and test_valid_move(self.bot)
        return valid

    def test(self):
        try:
            passed_all_tests = all(
                [
                    self.test_is_player_instance(),
                    self.test_name_not_null(),
                    self.test_not_none_on_start(),
                    self.test_valid_move(),
                ]
            )
        except NameError as e:
            raise TestNotPassedException(
                "You are using an undefined or forbidden function.\n" + str(e)
            )
        except Exception as e:
            traceback.print_exc()
            raise TestNotPassedException("Provided tests did not pass")
        if not passed_all_tests:
            raise TestNotPassedException("Provided tests did not pass")


if __name__ == "__main__":
    from perudo_game.players.player_demo import Player  # import your Bot HERE

    player_to_test = Player
    TestBot(player_to_test).test()
    print("All tests passed!")
