from dataclasses import dataclass

from playerInterface import PlayerInterface


@dataclass
class GameMove:
    number: int
    amount: int
    player_id: int=None

