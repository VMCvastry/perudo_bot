import time

import telegram

from perudo_game.game.gameMove import GameMove
from telegram.ext import CallbackContext
from perudo_game.game.game_info import GameInfo
from perudo_game.players import PlayerInterface

telegram_timeout_secs = 300


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
            return None, self.get_ending_status_as_JSON()
        else:
            return GameMove(number, amount), self.get_ending_status_as_JSON()
