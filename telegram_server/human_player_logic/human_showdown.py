from __future__ import annotations

import time

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
from threading import Thread

dices_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
        ],
        [
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
            InlineKeyboardButton("6", callback_data="6"),
        ],
        [
            InlineKeyboardButton("Call Bluff", callback_data="call_bluff"),
        ],
    ]
)


class ShowdownManager:
    def __init__(self):
        self.opponent_id = None
        self.next_move: list[int, int] | None = None
        self.number_to_bet_on = None
        self.is_time_to_ask_for_move = False
        self.game = None
        self.tread = None

    def choose_opponent(self, update: Update, context: CallbackContext):
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
            ui = TelegramUI(context, update.effective_chat.id)
            players = {
                0: TelegramPlayer(0, self),
                1: get_sandbox_bot(bot)(1),
            }
            self.game = Game(players, ui)
            self.tread = Thread(target=self.game.start)
            self.tread.start()
            # thread.join()

            self.wait()
            # context.bot.send_message(
            #     chat_id=update.effective_chat.id,
            #     text="your move:",
            #     reply_markup=dices_keyboard,
            # )
            return self.ask_for_move(context.bot, update.effective_chat.id)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="invalid id, try again"
            )
            return 0

    def wait(self):
        while not self.is_time_to_ask_for_move and not self.game.winner:
            time.sleep(0.5)
        self.is_time_to_ask_for_move = False

    def ask_for_move(self, bot, chat_id):
        if self.game.winner:
            self.tread.join()
            bot.send_message(
                chat_id=chat_id,
                text=f"player {self.game.winner[0]} won",
            )
            return ConversationHandler.END
        bot.send_message(
            chat_id=chat_id,
            text="your move:",
            reply_markup=dices_keyboard,
        )
        return 1

    def get_dice(self, update: Update, context: CallbackContext):
        print("get move")
        query = update.callback_query
        query.answer()
        n = query.data
        self.number_to_bet_on = int(n)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="place your bet:"
        )
        return 2

    def call_bluff(self, update: Update, context: CallbackContext):
        self.next_move = [None, None]
        self.wait()
        return self.ask_for_move(context.bot, update.effective_chat.id)

    def get_amount(self, update: Update, context: CallbackContext):
        amount = update.message.text
        self.next_move = [self.number_to_bet_on, int(amount)]
        self.wait()
        return self.ask_for_move(context.bot, update.effective_chat.id)


manager = ShowdownManager()
showdown_handler = ConversationHandler(
    entry_points=[CommandHandler("play", manager.choose_opponent)],
    states={
        0: [
            MessageHandler(Filters.text & ~Filters.command, manager.launch_duel),
        ],
        1: [
            CallbackQueryHandler(manager.get_dice, pattern=r"^\d$"),
            CallbackQueryHandler(manager.call_bluff, pattern=r"^call_bluff$"),
        ],
        2: [
            MessageHandler(Filters.text & ~Filters.command, manager.get_amount),
        ],
    },
    fallbacks=[
        CommandHandler("play", manager.choose_opponent)
    ],  # TODO what is fallbacks
)
