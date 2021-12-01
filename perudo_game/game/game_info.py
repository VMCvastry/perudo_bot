from dataclasses import dataclass

from .gameMove import GameMove
from .player_entity import PlayerEntity


@dataclass
class GameInfo:
    players: list[tuple[int, int]]  # [(player_id,number_of_dices),...]
    round: int
    moves_history: list[list[GameMove]]
    first_call: bool
