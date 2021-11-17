from abc import ABC, abstractmethod

from GameMove import GameMove
from gameStatus import GameStatus


class UI(ABC):
    @abstractmethod
    def show_header(self):
        pass

    @abstractmethod
    def show_summary(self, game: GameStatus):
        pass

    @abstractmethod
    def show_round(self, moves: list[GameMove]):
        pass

    @abstractmethod
    def show_round_check(self, game: GameStatus):
        pass

    @abstractmethod
    def show_players_dices(self, numbers: list[int]):
        pass

    @abstractmethod
    def show_result(self, result):
        pass
