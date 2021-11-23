from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from perudo_game.players import PlayerInterface


class PlayerEntity:
    def __init__(self, player: type[PlayerInterface], id):
        self.player = player
        # self.tokens = 21
        self.n_dices = 6
        self.numbers = []
        self.id = id
        self.status: str = "{}"

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers

    def __str__(self):
        return f"player: {self.id}, {self.n_dices} dices"
