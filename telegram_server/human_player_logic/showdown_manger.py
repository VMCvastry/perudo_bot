from __future__ import annotations

import time
from threading import Thread

from telegram.ext import CallbackContext, ConversationHandler

from bots import get_sandbox_bot
from database import Database
from perudo_game.game.dices_emoji import get_face_emoji
from perudo_game.game_core import Game
from telegram_server.human_player_logic.telegram_player import TelegramPlayer
from telegram_server.human_player_logic.telegram_ui import TelegramUI
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

dices_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(get_face_emoji(1), callback_data="1"),
            InlineKeyboardButton(get_face_emoji(2), callback_data="2"),
            InlineKeyboardButton(get_face_emoji(3), callback_data="3"),
        ],
        [
            InlineKeyboardButton(get_face_emoji(4), callback_data="4"),
            InlineKeyboardButton(get_face_emoji(5), callback_data="5"),
            InlineKeyboardButton(get_face_emoji(6), callback_data="6"),
        ],
        [
            InlineKeyboardButton("Call Bluff", callback_data="call_bluff"),
            InlineKeyboardButton("Call Spot On", callback_data="call_spot_on"),
        ],
    ]
)
amount_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("X 1", callback_data="1"),
            InlineKeyboardButton("X 2", callback_data="2"),
            InlineKeyboardButton("X 3", callback_data="3"),
        ],
        [
            InlineKeyboardButton("X 4", callback_data="4"),
            InlineKeyboardButton("X 5", callback_data="5"),
            InlineKeyboardButton("X 6", callback_data="6"),
        ],
        [
            InlineKeyboardButton("Change Face", callback_data="back"),
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
        self.interrupted = False
        self.db = Database()

    def choose_opponent(self, update: Update, context: CallbackContext):
        leaderboard = self.db.get_leaderboard()
        bot_keyboard = [
            [InlineKeyboardButton(str(bot), callback_data=str(bot.bot_id))]
            for bot in leaderboard
        ]
        bot_keyboard.append(
            [InlineKeyboardButton("Choose by ID", callback_data="choose_by_id")]
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Choose your opponent!",
            reply_markup=InlineKeyboardMarkup(bot_keyboard),
        )
        return 0

    def choose_opponent_by_id(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            f"Send your opponent id\nUse /leaderboard to see the available bots"
        )
        return 0

    def launch_duel(self, update: Update, context: CallbackContext):
        query = update.callback_query
        if not query:
            opponent_raw_id = update.message.text
            try:
                opponent_id = int(opponent_raw_id)
            except ValueError:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Id must be a number"
                )
                return 0
        else:
            query.answer()
            opponent_id = int(query.data)

        bot = self.db.get_bot(opponent_id)
        if bot:
            self.opponent_id = opponent_id
            self.bot = context.bot
            self.chat_id = update.effective_chat.id
            players = {
                0: TelegramPlayer,
                1: get_sandbox_bot(bot),
            }
            ui = TelegramUI(context, update.effective_chat.id, 0, players)
            self.game = Game(players, ui, [(0, TelegramPlayer(self))])
            self.thread = Thread(target=self.game.start)
            self.thread.start()
            self.wait()
            return self.ask_for_move(update, context, no_edit=True)
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

    def ask_for_move(self, update: Update, context: CallbackContext, no_edit=False):
        if self.game.winner:
            self.thread.join()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"player {self.game.winner[0]} won",
            )
            self.timed_out = True
            return ConversationHandler.END
        if self.game.exception:
            self.thread.join()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Game interrupted, an error occurred with player {self.game.exception.player_id}:\n{str(self.game.exception)}",
            )
            self.timed_out = True
            return ConversationHandler.END

        if no_edit:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Choose a dice face to rise the bet on\nOtherwise Call the bluff",
                reply_markup=dices_keyboard,
            )
        else:
            query = update.callback_query
            query.edit_message_text(
                f"Choose a dice face to rise the bet on\nOtherwise Call the bluff"
            )
            query.edit_message_reply_markup(reply_markup=dices_keyboard)
        return 1

    def get_dice(self, update: Update, context: CallbackContext):
        if self.timed_out:
            return self.call_timeout()
        print("get move")
        query = update.callback_query
        query.answer()
        n = query.data
        self.number_to_bet_on = int(n)
        query.edit_message_text(f"How many {get_face_emoji(self.number_to_bet_on)}?")
        query.edit_message_reply_markup(reply_markup=amount_keyboard)
        return 2

    def call_bluff(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.timed_out:
            return self.call_timeout()
        self.next_move = ["call_bluff", None]
        self.wait()
        return self.ask_for_move(update, context, no_edit=True)

    def call_spot_on(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.timed_out:
            return self.call_timeout()
        self.next_move = ["call_spot_on", None]
        self.wait()
        return self.ask_for_move(update, context, no_edit=True)

    def get_amount(self, update: Update, context: CallbackContext):
        if self.timed_out:
            return self.call_timeout()
        query = update.callback_query
        if not query:
            amount = update.message.text
            try:
                amount = int(amount)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Amount must be a positive number",
                )
                return 2
        else:
            query.answer()
            amount = int(query.data)
        self.next_move = [self.number_to_bet_on, amount]
        self.wait()
        return self.ask_for_move(update, context, no_edit=True)

    def back_to_face(self, update: Update, context: CallbackContext):
        update.callback_query.answer()

        return 1

    def kill_game(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The game was Interrupted",
        )
        self.interrupted = True
        self.thread.join()
        return ConversationHandler.END
