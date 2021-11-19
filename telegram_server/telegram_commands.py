from telegram import Update
from telegram.ext import CallbackContext
import telegram

from database import Database


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="see your stats, see your bots,upload bot,play",
    )


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def callback(update: Update, context: CallbackContext):
    print("f")


# lambda x: x.victory / (x.victory + x.defeat)
def get_leaderboard(update: Update, context: CallbackContext):
    db_path = "./bots.db"
    db = Database(db_path)
    bots = db.get_all_bots()
    leaderboard = sorted(bots, key=lambda x: x.get_win_ratio(), reverse=True)
    [print(x) for x in leaderboard]
    leaderboard_format = "\n".join([str(x) for x in leaderboard])
    context.bot.send_message(chat_id=update.effective_chat.id, text=leaderboard_format)


k = telegram.InlineKeyboardButton(text="awdaw", callback_data="ciao")
keyboard = telegram.InlineKeyboardMarkup([[k]])

# def upload_bot(update: Update, context: CallbackContext):
#     # context.bot.
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text="a", reply_markup=keyboard
#     )
