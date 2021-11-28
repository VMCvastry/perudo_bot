from __future__ import annotations
from telegram_server.human_player_logic.showdown_manger import ShowdownManager
from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

managers = {}


class Manager:
    # associate a Showdown Manager to each chat id
    def __init__(self):
        self.active_chats: dict[int:ShowdownManager] = {}  # TODO check for memory leak

    def choose_opponent(self, update: Update, context: CallbackContext):
        self.active_chats[update.effective_chat.id] = ShowdownManager()
        return self.active_chats[update.effective_chat.id].choose_opponent(
            update, context
        )

    def launch_duel(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].launch_duel(update, context)

    def get_dice(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].get_dice(update, context)

    def call_bluff(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].call_bluff(update, context)

    def get_amount(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].get_amount(update, context)


manager = Manager()
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
        # -2: [MessageHandler(Filters.all, manager.call_timeout)],
    },
    fallbacks=[
        CommandHandler("play", manager.choose_opponent)
    ],  # TODO what is fallbacks
    # conversation_timeout=10,
)
