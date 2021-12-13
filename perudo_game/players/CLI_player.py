from perudo_game.exceptions import raise_exception_if_invalid_move
from perudo_game.game.gameMove import GameMove
import json
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class HumanPlayer(PlayerInterface):
    def __init__(self, player_status_JSON):
        super().__init__(player_status_JSON)

    def move(self, status: GameInfo, numbers: list[int]) -> GameMove:
        n = input("amount")
        if not n:
            return None
        else:

            number = input("number:")
            move = GameMove(int(number), int(n))
            raise_exception_if_invalid_move(status, move)
            return move

    @staticmethod
    def get_player_name() -> str:
        return "cli_player"
