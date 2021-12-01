from __future__ import annotations

import time
from threading import Thread


from telegram.ext import CallbackContext, ConversationHandler

from bots import get_sandbox_bot
from database import Database
from perudo_game.game_core import Game
from telegram_server.human_player_logic.telegram_player import TelegramPlayer
from telegram_server.human_player_logic.telegram_ui import TelegramUI
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

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
        self.thread = None
        self.bot = None
        self.chat_id = None
        self.timed_out = False

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
        db = Database()
        bot = db.get_bot(opponent_id)
        if bot:
            self.opponent_id = opponent_id
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="game is starting"
            )
            self.bot = context.bot
            self.chat_id = update.effective_chat.id
            ui = TelegramUI(context, update.effective_chat.id, 0)
            players = {
                0: TelegramPlayer,
                1: get_sandbox_bot(bot),
            }
            self.game = Game(players, ui, [(0, TelegramPlayer(self))])
            self.thread = Thread(target=self.game.start)
            self.thread.start()
            self.wait()
            return self.ask_for_move(context.bot, update.effective_chat.id)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="invalid id, try again"
            )
            return 0

    def wait(self):
        while (
                not self.is_time_to_ask_for_move
                and not self.game.winner
                and not self.game.exception
        ):
            time.sleep(0.5)
        self.is_time_to_ask_for_move = False

    def call_timeout(self):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=f"Waited for too long, game interrupted",
        )
        self.timed_out = True
        return ConversationHandler.END

    def show_error(self, e: Exception):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=str(e),
        )

    def ask_for_move(self, bot, chat_id):
        if self.game.winner:
            self.thread.join()
            bot.send_message(
                chat_id=chat_id,
                text=f"player {self.game.winner[0]} won",
            )
            self.timed_out = True
            return ConversationHandler.END
        if self.game.exception:
            self.thread.join()
            bot.send_message(
                chat_id=chat_id,
                text=f"Game interrupted, an error occurred with player {self.game.exception.player_id}:\n{str(self.game.exception)}",
            )
            self.timed_out = True
            return ConversationHandler.END
        bot.send_message(
            chat_id=chat_id,
            text="your move:",
            reply_markup=dices_keyboard,
        )
        return 1

    def get_dice(self, update: Update, context: CallbackContext):
        if self.timed_out:
            return self.call_timeout()
        print("get move")
        query = update.callback_query
        query.answer()
        n = query.data
        self.number_to_bet_on = int(n)
        query.edit_message_text(f"how many {n}?")
        return 2

    def call_bluff(self, update: Update, context: CallbackContext):
        if self.timed_out:
            return self.call_timeout()
        self.next_move = [None, None]
        self.wait()
        return self.ask_for_move(context.bot, update.effective_chat.id)

    def get_amount(self, update: Update, context: CallbackContext):
        if self.timed_out:
            return self.call_timeout()
        amount = update.message.text
        self.next_move = [self.number_to_bet_on, int(amount)]
        self.wait()
        return self.ask_for_move(context.bot, update.effective_chat.id)
