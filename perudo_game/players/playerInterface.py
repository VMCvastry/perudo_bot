from abc import ABC, abstractmethod

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo


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


def pp():
    print("ciao")
