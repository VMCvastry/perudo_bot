from collections import Counter

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class BotTest(PlayerInterface):
    def __init__(self, player_id):
        self.name = "Bot_" + str(player_id)
        self.numbers = []

    def get_player_name(self) -> str:
        return self.name

    def make_a_move(self, status: GameInfo) -> GameMove:
        print("MOVING")
        numbers = Counter(self.numbers)
        value, n = numbers.most_common(1)[0]

        if status.first_call:
            return GameMove(value, n)

    #     else:
    #         if last.amount >= n:
    #             if random.random() > 0.5:
    #                 return GameMove(value, last.amount + 1)
    #             return None
    #         else:
    #             return GameMove(value, n)
    #
    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers
