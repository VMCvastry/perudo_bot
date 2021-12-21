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

    def choose_opponent_by_id(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].choose_opponent_by_id(
            update, context
        )

    def launch_duel(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].launch_duel(update, context)

    def get_dice(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].get_dice(update, context)

    def call_bluff(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].call_bluff(update, context)

    def call_spot_on(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].call_spot_on(update, context)

    def get_amount(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].get_amount(update, context)

    def ask_for_move(self, update: Update, context: CallbackContext):
        return self.active_chats[update.effective_chat.id].ask_for_move(update, context)

    def kill_game(self, update: Update, context: CallbackContext):
        manager_to_kill = self.active_chats[update.effective_chat.id]
        del self.active_chats[update.effective_chat.id]
        return manager_to_kill.kill_game(update, context)


manager = Manager()
showdown_handler = ConversationHandler(
    entry_points=[CommandHandler("play", manager.choose_opponent)],
    states={
        0: [
            CallbackQueryHandler(
                manager.choose_opponent_by_id, pattern=r"choose_by_id"
            ),
            MessageHandler(Filters.text & ~Filters.command, manager.launch_duel),
            CallbackQueryHandler(manager.launch_duel, pattern=r"^\d+$"),
        ],
        1: [
            CallbackQueryHandler(manager.get_dice, pattern=r"^\d$"),
            CallbackQueryHandler(manager.call_bluff, pattern=r"^call_bluff$"),
            CallbackQueryHandler(manager.call_spot_on, pattern=r"^call_spot_on$"),
        ],
        2: [
            CallbackQueryHandler(manager.get_amount, pattern=r"^\d$"),
            CallbackQueryHandler(manager.ask_for_move, pattern=r"^back$"),
            MessageHandler(Filters.text & ~Filters.command, manager.get_amount),
        ],
        # -2: [MessageHandler(Filters.all, manager.call_timeout)],
    },
    fallbacks=[
        CommandHandler("stop", manager.kill_game)
    ],  # todo error when called before game start
    # conversation_timeout=10,
    # per_message=False,
)
