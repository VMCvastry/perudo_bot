from telegram import Update
from telegram.ext import CallbackContext
import telegram, requests


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="see your stats, see your bots,upload bot,play",
    )


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def callback(update: Update, context: CallbackContext):
    print("f")


k = telegram.InlineKeyboardButton(text="awdaw", callback_data="ciao")
keyboard = telegram.InlineKeyboardMarkup([[k]])

# def upload_bot(update: Update, context: CallbackContext):
#     # context.bot.
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text="a", reply_markup=keyboard
#     )
