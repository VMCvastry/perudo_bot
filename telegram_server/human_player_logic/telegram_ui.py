from telegram.ext import CallbackContext

from perudo_game.game.gameStatus import GameStatus
from perudo_game.ui.ui_interface import UI
from perudo_game.game.gameMove import GameMove


class TelegramUI(UI):
    def __init__(self, context: CallbackContext, chat_id):
        self.bot = context.bot
        self.chat_id = chat_id

    def show_header(self):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="header",
        )

    def show_summary(self, game: GameStatus):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="summary\n" + "\n".join([str(p) for p in game.players]),
        )

    def show_round(self, moves: list[GameMove]):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="pastmoves\n" + str(moves[-1]),
        )

    def show_round_check(self, game: GameStatus):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="the dices are\n" + str([p.numbers for p in game.players]),
        )
        print("the dices are")
        print([p.numbers for p in game.players])

    def show_players_dices(self, numbers: list[int]):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="your dices:\n" + str(numbers),
        )
        print("your dices:")
        print(numbers)

    def show_result(self, result):
        self.bot.send_message(
            chat_id=self.chat_id,
            text="result:\n" + str(result),
        )
        print(result)
        input("continue")
