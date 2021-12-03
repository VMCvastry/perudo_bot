import traceback

from telegram import Update
from telegram.ext import CallbackContext
import telegram, requests
from bots import get_new_bot
from bots.test_player import TestNotPassedException
from database import Database
from telegram_server.ranking import rank_and_save_bot


def download_file(url):
    res = requests.get(url).text
    return res


def upload_bot(update: Update, context: CallbackContext):
    db_path = "../bots.db"
    db = Database()
    document = update.message.document
    name = document.file_name
    file_id = document.file_id
    file_path = context.bot.getFile(file_id).file_path
    code = download_file(file_path)
    user_id = update.effective_chat.id
    if db.get_user(user_id) is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not present in the Database, use /start to register",
        )
        return
    try:
        bot = get_new_bot(user_id, code)
    except TestNotPassedException as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your bot does not meet the guidelines and did not pass the provided test, use /upload to get more info on the guidelines:\n"
            + str(e),
        )
        return
    except Exception as e:
        traceback.print_exc()
        return
    if bot:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="ranking staterd"
        )
        win_ratio = rank_and_save_bot(bot)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(win_ratio * 100) + "% victories"
        )


# download_file(
#     "https://api.telegram.org/file/bot2108006502:AAHYD7DiT-d0nGpakTnu4GuDGJfcy0G0e70/documents/file_2.py"
# )
