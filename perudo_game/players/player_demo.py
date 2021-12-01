import random, json, time
from collections import Counter

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class DemoBot(PlayerInterface):
    @staticmethod
    def get_player_name() -> str:
        return "Bot_1"

    def move(self, status: GameInfo, numbers) -> GameMove:
        numbers = Counter(numbers)
        value, n = numbers.most_common(1)[0]
        if status.first_call:
            return GameMove(value, n)
        else:
            last = status.moves_history[-1][-1]
            if last.amount >= n:
                if random.random() > 0.5:
                    return GameMove(value, last.amount + 1)
                return None
            else:
                return GameMove(value, n)
