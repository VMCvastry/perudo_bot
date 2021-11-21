import time

import telegram

from perudo_game.game.gameMove import GameMove
from telegram.ext import CallbackContext
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


# k = telegram.InlineKeyboardButton(text=str(x), callback_data={number})


class TelegramPlayer(PlayerInterface):
    # TODO player_id in abstract interface
    def __init__(self, player_id: int, context):
        self.name = "Bot_" + str(player_id)
        self.numbers = []
        self.context = context

    def get_player_name(self) -> str:
        return self.name

    def make_a_move(self, status: GameInfo) -> GameMove:
        print("IN")
        self.context.is_time_to_ask_for_move = True
        while not self.context.next_move:
            time.sleep(0.5)
        number, amount = self.context.next_move
        print("next move", number, amount)
        self.context.next_move = None
        if not number:
            return None
        else:
            return GameMove(number, amount)

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers
