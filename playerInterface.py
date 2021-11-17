from abc import ABC, abstractmethod

from GameMove import GameMove
from gameStatus import GameStatus


class PlayerInterface(ABC):
    @abstractmethod
    def get_player_name(self) -> str:
        pass

    @abstractmethod
    def make_a_move(self, status: GameStatus) -> GameMove:
        pass

    @abstractmethod
    def set_rolled_dices(self, numbers: list[int]):
        pass
