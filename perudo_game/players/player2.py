from perudo_game.game.gameMove import GameMove
import json
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


class HumanPlayer(PlayerInterface):
    def __init__(self, player_status_JSON):
        super().__init__(player_status_JSON)

    @staticmethod
    def get_player_name() -> str:
        return "cli_player"

    def make_a_move(self, status: GameInfo, numbers) -> (GameMove, str):
        n = input("amount")
        if not n:
            return None, self.get_ending_status_as_JSON()
        else:

            number = input("number:")
            return GameMove(int(number), int(n)), self.get_ending_status_as_JSON()

    def get_ending_status_as_JSON(self) -> str:
        return json.dumps(self.status)
