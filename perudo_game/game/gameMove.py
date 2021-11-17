from dataclasses import dataclass


@dataclass
class GameMove:
    number: int
    amount: int
    player_id: int = None
