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
        # Return bot name as a Static String, Eg:
        # return "Pippo"
        pass

    # DO NOT OVERRIDE
    def make_a_move(self, status: GameInfo, numbers: list[int]) -> (GameMove, str):
        return self.move(status, numbers), self.get_ending_status_as_JSON()

    # DO NOT OVERRIDE
    def get_ending_status_as_JSON(self) -> str:
        return json.dumps(self.status)

    @abstractmethod
    def move(self, status: GameInfo, numbers: list[int]) -> GameMove:
        pass
