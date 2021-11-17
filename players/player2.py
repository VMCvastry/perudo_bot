from GameMove import GameMove
import random
from gameStatus import GameStatus
from players import PlayerInterface


class HumanPlayer(PlayerInterface):
    # TODO player_id in abstract interface
    def __init__(self, player_id: int):
        self.name = "Bot_" + str(player_id)
        self.numbers = []

    def get_player_name(self) -> str:
        return self.name

    def make_a_move(self, status: GameStatus) -> GameMove:
        n = input("amount")
        if not n:
            return None
        else:

            number = input("number:")
            return GameMove(int(number), int(n))

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers
