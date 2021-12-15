from telegram import Update
from telegram.ext import CallbackContext
from telegram_server.rules import rules
from database import Database


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text + " is not a valid command",
    )


def callback(update: Update, context: CallbackContext):
    print("f")


# lambda x: x.victory / (x.victory + x.defeat)
def get_leaderboard(update: Update, context: CallbackContext):
    db_path = "../bots.db"
    db = Database()
    bots = db.get_all_bots()
    leaderboard = sorted(bots, key=lambda x: x.get_win_ratio(), reverse=True)
    users = db.get_all_user()
    for bot in bots:
        bot.username = users[bot.user_id].get_name()
    # [print(x) for x in leaderboard]
    leaderboard_format = "\n".join([str(x) for x in leaderboard])
    context.bot.send_message(chat_id=update.effective_chat.id, text=leaderboard_format)


def show_upload_info(update: Update, context: CallbackContext):
    upload_info = """To learn how to write your code go to https://github.com/VMCvastry/perudo_bot, unfortunately at the moment Only python 3 is supported.
Once you have written your Bot just drop the .py in this chat."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=upload_info)


def show_help(update: Update, context: CallbackContext):
    upload_info = """This bot allows you to Code you very own bot to play The Perudo Dice game, /game_info to read the game rules.\n
Use /leaderboard to see who is leading the game and use /play to play against one of the bots in the leaderboard.\n
Use /upload to get more info on how to write your bot."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=upload_info)


def show_rules(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=rules)


# def upload_bot(update: Update, context: CallbackContext):
#     # context.bot.
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text="a", reply_markup=keyboard
#     )
# {
#     "update_id": 244751907,
#     "message": {
#         "date": 1637233040,
#         "caption_entities": [],
#         "new_chat_members": [],
#         "document": {
#             "file_size": 111051,
#             "file_name": "CV_EN_main.pdf",
#             "file_id": "BQACAgQAAxkBAAMXYZYxjw5b-Tbws9KQBNdmtlRr5Z4AAmYMAAJM4rFQdEONGzv7lAYiBA",
#             "file_unique_id": "AgADZgwAAkzisVA",
#             "thumb": {
#                 "file_size": 19030,
#                 "file_id": "AAMCBAADGQEAAxdhljGPDlv5NvCz0pAE12a2VGvlngACZgwAAkzisVB0Q40bO_uUBgEAB20AAyIE",
#                 "file_unique_id": "AQADZgwAAkzisVBy",
#                 "height": 320,
#                 "width": 226,
#             },
#             "mime_type": "application/pdf",
#         },
#         "delete_chat_photo": False,
#         "supergroup_chat_created": False,
#         "group_chat_created": False,
#         "photo": [],
#         "chat": {
#             "username": "VMCvastry",
#             "id": 723468787,
#             "last_name": "Massimo",
#             "first_name": "Valerio",
#             "type": "private",
#         },
#         "new_chat_photo": [],
#         "entities": [],
#         "message_id": 23,
#         "channel_chat_created": False,
#         "from": {
#             "id": 723468787,
#             "username": "VMCvastry",
#             "language_code": "en",
#             "first_name": "Valerio",
#             "is_bot": False,
#             "last_name": "Massimo",
#         },
#     },
# }
