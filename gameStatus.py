from GameMove import GameMove
from player_entity import PlayerEntity


# TODO pass copy to user
class GameStatus:
    def __init__(self, players: list[PlayerEntity]):
        self.players: list[PlayerEntity] = players
        self.turn: int = 0
        self.round: int = 0
        self.moves_history: list[[GameMove]] = [[]]

    def new_round(self):
        self.moves_history.append([])

    def add_move(self, move: GameMove):
        self.moves_history[-1].append(move)

    def last_move(self) -> GameMove:
        return self.moves_history[-1][-1]

    def next_id(self, id):
        return (id + 1) % len(self.players)
