from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from database import Database
from user_class import User


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    #     logger.info("User %s started the conversation.", user.first_name)
    print(user.username, user.first_name)
    db_path = "../bots.db"
    db = Database()
    user_id = update.effective_chat.id
    if db.get_user(user_id):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Welcome Back",
        )
        return ConversationHandler.END
    else:
        db.add_user(User(user_id))
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data="disclose_name"),
                    InlineKeyboardButton("be Anon", callback_data="be_anon"),
                ]
            ]
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Welcome, do you want to be shown in leadersboards as your nick?",
            reply_markup=keyboard,
        )
        return 0


def disclose_name(update: Update, context: CallbackContext):
    db = Database()
    user_id = update.effective_chat.id
    user = update.effective_user
    db.set_username(
        user_id, user.username if user.username is not None else user.first_name
    )
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="You choose to show your name,Everyone will know who is the best"
    )
    return ConversationHandler.END


def be_anon(update: Update, context: CallbackContext):
    db = Database()
    user_id = update.effective_chat.id
    db.set_username(user_id, "Anon")
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="You choose to be Anonymous,You will fight in the darkness"
    )
    return ConversationHandler.END


user_setup_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        0: [
            CallbackQueryHandler(disclose_name, pattern="^disclose_name$"),
            CallbackQueryHandler(be_anon, pattern="^be_anon$"),
        ]
    },
    fallbacks=[CommandHandler("start", start)],
)
