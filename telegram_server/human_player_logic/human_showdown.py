from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

from bots import get_sandbox_bot
from database import Database
from perudo_game.game_core import Game
from telegram_server.human_player_logic.telegram_player import TelegramPlayer
from telegram_server.human_player_logic.telegram_ui import TelegramUI


class ShowdownManager:
    def __init__(self):
        self.opponent_id = None

    def choose_opponent(self, update: Update, context: CallbackContext):
        # keyboard = InlineKeyboardMarkup(
        #     [
        #         [
        #             InlineKeyboardButton("4", callback_data="4"),
        #             InlineKeyboardButton("5", callback_data="5"),
        #         ]
        #     ]
        # )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="choose your opponent id",
            # reply_markup=keyboard,
        )
        return 0

    def launch_duel(self, update: Update, context: CallbackContext):
        opponent_raw_id = update.message.text
        opponent_id = int(opponent_raw_id)  # TODO try catch
        db = Database("../bots.db")
        bot = db.get_bot(opponent_id)
        if bot:
            self.opponent_id = opponent_id
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
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="invalid id, try again"
            )
            return 0


manager = ShowdownManager()
showdown_handler = ConversationHandler(
    entry_points=[CommandHandler("play", manager.choose_opponent)],
    states={
        0: [
            MessageHandler(Filters.text & ~Filters.command, manager.launch_duel),
        ]
    },
    fallbacks=[
        CommandHandler("play", manager.choose_opponent)
    ],  # TODO what is fallbacks
)
