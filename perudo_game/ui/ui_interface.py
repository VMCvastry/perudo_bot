from abc import ABC, abstractmethod

from perudo_game.game.gameMove import GameMove
from perudo_game.game.gameStatus import GameStatus


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
    def show_players_dices(self, numbers: list[int], player_id):
        pass

    @abstractmethod
    def show_result(self, result):
        pass

    @abstractmethod
    def show_player_move(self, move, player_id):
        pass

    @abstractmethod
    def show_winner(self, player_id):
        pass
