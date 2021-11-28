import time

import telegram

from perudo_game.game.gameMove import GameMove
from telegram.ext import CallbackContext
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface

telegram_timeout_secs = 500


class TelegramPlayer(PlayerInterface):
    # TODO player_id in abstract interface
    def __init__(self, manager):
        super().__init__("{}")
        self.manager = manager

    def get_player_name(self) -> str:
        return "Telegram"

    def move(self, status: GameInfo, numbers) -> GameMove:
        print("IN")
        self.manager.is_time_to_ask_for_move = True
        start_time = time.time()
        while (
            not self.manager.next_move
            and (time.time() - start_time) < telegram_timeout_secs
        ):
            time.sleep(0.5)
        if not self.manager.next_move:
            self.manager.call_timeout()
            raise TimeoutError
        number, amount = self.manager.next_move
        print("next move", number, amount)
        self.manager.next_move = None
        if not number:
            return None
        else:
            return GameMove(number, amount)
