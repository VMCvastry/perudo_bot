from telegram import Update
from telegram.ext import CallbackContext

from bots import get_sandbox_bot
from database import Database
from perudo_game.game_core import Game
from telegram_server.telegram_player import TelegramPlayer
from telegram_server.telegram_ui import TelegramUI


def launch_duel(update: Update, context: CallbackContext):
    bot_id = context.args[0]
    db = Database("./bots.db")
    bot = db.get_bot(4)
    if bot:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="game is starting"
        )
        ui = TelegramUI()
        players = {
            0: TelegramPlayer(0),
            1: get_sandbox_bot(bot)(1),
        }
        Game(players, ui).start()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="invalid id")


# db = Database("../bots.db")
# bot = db.get_bot(4)
# print(bot.name)
