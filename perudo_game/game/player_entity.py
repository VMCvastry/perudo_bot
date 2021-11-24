from __future__ import annotations

from typing import TYPE_CHECKING

from timeout_manager import execute_with_timeout

if TYPE_CHECKING:
    from perudo_game.game.gameMove import GameMove
    from perudo_game.game.game_info import GameInfo
    from perudo_game.players import PlayerInterface


class PlayerEntity:
    def __init__(self, player: type[PlayerInterface], player_id):
        self.player = player
        # self.tokens = 21
        self.n_dices = 6
        self.numbers = []
        self.id = player_id
        self.status: str = "{}"
        self.timeout = True

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers

    def make_move(self, info: GameInfo) -> GameMove:
        if self.timeout:
            move, self.status = execute_with_timeout(
                create_player_and_get_move,
                (self.player, self.status, self.numbers, info),
                timeout=self.timeout,
            )
        else:
            move, self.status = create_player_and_get_move(
                self.player, self.status, self.numbers, info
            )
        return move

    def __str__(self):
        return f"player: {self.id}, {self.n_dices} dices"


def create_player_and_get_move(player, status, numbers, info):
    return player(status).make_a_move(info, numbers)
