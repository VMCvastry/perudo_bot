from abc import ABC, abstractmethod

from gameMove import GameMove
from game_info import GameInfo


class PlayerInterface(ABC):
    @abstractmethod
    def get_player_name(self) -> str:
        pass

    @abstractmethod
    def make_a_move(self, status: GameInfo) -> GameMove:
        pass

    @abstractmethod
    def set_rolled_dices(self, numbers: list[int]):
        pass
