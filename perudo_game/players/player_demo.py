import random, json, time
from collections import Counter

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class Player(PlayerInterface):
    @staticmethod
    def get_player_name() -> str:
        return "Demo_Bot"

    def move(self, status: GameInfo, numbers) -> GameMove:
        numbers_counter = Counter(numbers)
        value, n = numbers_counter.most_common(1)[0]
        if status.first_call:
            return GameMove(value, n)
        else:
            last = status.moves_history[-1][-1]
            if last.number == 1:
                return GameMove(1, last.amount + 1)
            if last.amount >= n:
                if random.random() > 0.5:
                    return GameMove(value, last.amount + 1)
                return GameMove.call_bluff()
            else:
                return GameMove(value, n)
