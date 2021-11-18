from telegram import Update
from telegram.ext import CallbackContext
import telegram, requests
from bots import test_and_save_new_bot
from database import Database


def download_file(url):
    res = requests.get(url).text
    return res


def upload_bot(update: Update, context: CallbackContext):
    db = Database("./bots.db")
    document = update.message.document
    name = document.file_name
    file_id = document.file_id
    file_path = context.bot.getFile(file_id).file_path
    code = download_file(file_path)
    user_id = update.effective_chat.id
    response = test_and_save_new_bot(db, user_id, code)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# download_file(
#     "https://api.telegram.org/file/bot2108006502:AAHYD7DiT-d0nGpakTnu4GuDGJfcy0G0e70/documents/file_2.py"
# )
