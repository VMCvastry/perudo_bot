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

    def get_player_name(self) -> str:
        return self.name

    def make_a_move(self, status: GameInfo) -> GameMove:

        keyboard = telegram.InlineKeyboardMarkup([[k]])
        n = input("amount")
        if not n:
            return None
        else:

            number = input("number:")
            return GameMove(int(number), int(n))

    def set_rolled_dices(self, numbers: list[int]):
        self.numbers = numbers
