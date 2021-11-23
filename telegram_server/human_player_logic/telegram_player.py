import time

import telegram

from perudo_game.game.gameMove import GameMove
from telegram.ext import CallbackContext
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface


# k = telegram.InlineKeyboardButton(text=str(x), callback_data={number})


class TelegramPlayer(PlayerInterface):
    manager = None
    # TODO player_id in abstract interface
    def __init__(self, player_status):
        super().__init__(player_status)

    def get_player_name(self) -> str:
        return "Telegram"

    def make_a_move(self, status: GameInfo, numbers) -> (GameMove, str):
        print("IN")
        self.manager.is_time_to_ask_for_move = True
        while not self.manager.next_move:
            time.sleep(0.5)
        number, amount = self.manager.next_move
        print("next move", number, amount)
        self.manager.next_move = None
        if not number:
            return None, self.get_ending_status_as_JSON()
        else:
            return GameMove(number, amount), self.get_ending_status_as_JSON()
