import traceback

from telegram import Update
from telegram.ext import CallbackContext
import telegram, requests
from bots import get_new_bot
from database import Database
from ranking import rank_and_save_bot


def download_file(url):
    res = requests.get(url).text
    return res


def upload_bot(update: Update, context: CallbackContext):
    db_path = "./bots.db"
    # db = Database(db_path)
    document = update.message.document
    name = document.file_name
    file_id = document.file_id
    file_path = context.bot.getFile(file_id).file_path
    code = download_file(file_path)
    user_id = update.effective_chat.id
    try:
        bot = get_new_bot(user_id, code)
    except Exception as e:
        traceback.print_exc()
        return
    if bot:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="ranking staterd"
        )
        win_ratio = rank_and_save_bot(bot, db_path)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(win_ratio) + "% victories"
        )


# download_file(
#     "https://api.telegram.org/file/bot2108006502:AAHYD7DiT-d0nGpakTnu4GuDGJfcy0G0e70/documents/file_2.py"
# )
