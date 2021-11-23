import random, json, time
from collections import Counter

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class Bot1(PlayerInterface):
    # TODO player_id in abstract interface
    def __init__(self, player_status_JSON):
        super().__init__(player_status_JSON)

    @staticmethod
    def get_player_name() -> str:
        return "Bot_1"

    def make_a_move(self, status: GameInfo, numbers) -> (GameMove, str):
        print("MOVING")
        numbers = Counter(numbers)
        value, n = numbers.most_common(1)[0]
        if status.first_call:
            return GameMove(value, n), self.get_ending_status_as_JSON()
        else:
            last = status.moves_history[-1][-1]
            if last.amount >= n:
                if random.random() > 0.5:
                    return (
                        GameMove(value, last.amount + 1),
                        self.get_ending_status_as_JSON(),
                    )
                return None, self.get_ending_status_as_JSON()
            else:
                return GameMove(value, n), self.get_ending_status_as_JSON()

    def get_ending_status_as_JSON(self) -> str:
        return json.dumps(self.status)
