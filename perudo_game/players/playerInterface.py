import json
from abc import ABC, abstractmethod

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo


class PlayerInterface(ABC):
    def __init__(self, player_status_JSON):
        self.status = json.loads(player_status_JSON)

    @staticmethod
    @abstractmethod
    def get_player_name() -> str:
        pass

    @abstractmethod
    def make_a_move(self, status: GameInfo, numbers: list[int]) -> (GameMove, str):
        pass

    def get_ending_status_as_JSON(self) -> str:
        return json.dumps(self.status)
