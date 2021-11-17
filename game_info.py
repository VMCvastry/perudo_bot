from dataclasses import dataclass

from gameMove import GameMove
from player_entity import PlayerEntity


@dataclass
class GameInfo:
    players: list[PlayerEntity]
    round: int
    moves_history: list[[GameMove]]
    first_call: bool
