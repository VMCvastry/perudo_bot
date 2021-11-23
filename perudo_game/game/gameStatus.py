from copy import deepcopy

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from .player_entity import PlayerEntity


# TODO pass copy to user
class GameStatus:
    def __init__(self, players: list[PlayerEntity]):
        self.players: list[PlayerEntity] = players
        self.round: int = 0  # TODO use
        self.moves_history: list[[GameMove]] = [[]]

    def get_game_info(self) -> GameInfo:
        return GameInfo(  # todo DEEP coppy
            # deepcopy(self.players),
            self.players,
            self.round,
            # deepcopy(self.moves_history),
            self.moves_history,
            self.last_move() == None,
        )

    def new_round(self):
        self.moves_history.append([])

    def add_move(self, move: GameMove):
        self.moves_history[-1].append(move)

    def last_move(self) -> GameMove:
        if not self.moves_history[-1]:
            return None
        return self.moves_history[-1][-1]

    def next_id(self, id):
        return (id + 1) % len(self.players)

    def last_id(self, id):
        return (id - 1) % len(self.players)
