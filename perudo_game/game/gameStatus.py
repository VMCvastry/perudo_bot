from copy import deepcopy

from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
from .player_entity import PlayerEntity


def get_index(array, id):
    for i, player in enumerate(array):
        if player.id == id:
            return i


class GameStatus:
    def __init__(self, players: list[PlayerEntity]):
        self.players: list[PlayerEntity] = players
        self.round: int = 0
        self.moves_history: list[[GameMove]] = [[]]

    def get_game_info(self) -> GameInfo:
        return GameInfo(
            [(p.id, p.n_dices) for p in self.players],
            self.round,
            deepcopy(self.moves_history),
            self.last_move() is None,
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
        index = get_index(self.players, id)
        new_index = (index + 1) % len(self.players)
        return self.players[new_index].id

    def last_id(self, id):
        return (id - 1) % len(self.players)
