from telegram_server.telegram_commands import start, echo, callback
from telegram_server.telegram_token import token
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    Updater,
)

# t_bot = telegram.Bot(token=token)
# print(t_bot.get_me())
# while 1:
#     updates = t_bot.get_updates()
#     print(updates[-1])
#     input()
from telegram_server.upload_bot import upload_bot

updater = Updater(token=token)

dispatcher = updater.dispatcher

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# upload_handler = CommandHandler("upload", upload_bot)
# dispatcher.add_handler(upload_handler)

callback_handler = CallbackQueryHandler(callback)
dispatcher.add_handler(callback_handler)

doc_handler = MessageHandler(Filters.document, upload_bot)
dispatcher.add_handler(doc_handler)

updater.start_polling()
{
    "update_id": 244751907,
    "message": {
        "date": 1637233040,
        "caption_entities": [],
        "new_chat_members": [],
        "document": {
            "file_size": 111051,
            "file_name": "CV_EN_main.pdf",
            "file_id": "BQACAgQAAxkBAAMXYZYxjw5b-Tbws9KQBNdmtlRr5Z4AAmYMAAJM4rFQdEONGzv7lAYiBA",
            "file_unique_id": "AgADZgwAAkzisVA",
            "thumb": {
                "file_size": 19030,
                "file_id": "AAMCBAADGQEAAxdhljGPDlv5NvCz0pAE12a2VGvlngACZgwAAkzisVB0Q40bO_uUBgEAB20AAyIE",
                "file_unique_id": "AQADZgwAAkzisVBy",
                "height": 320,
                "width": 226,
            },
            "mime_type": "application/pdf",
        },
        "delete_chat_photo": False,
        "supergroup_chat_created": False,
        "group_chat_created": False,
        "photo": [],
        "chat": {
            "username": "VMCvastry",
            "id": 723468787,
            "last_name": "Massimo",
            "first_name": "Valerio",
            "type": "private",
        },
        "new_chat_photo": [],
        "entities": [],
        "message_id": 23,
        "channel_chat_created": False,
        "from": {
            "id": 723468787,
            "username": "VMCvastry",
            "language_code": "en",
            "first_name": "Valerio",
            "is_bot": False,
            "last_name": "Massimo",
        },
    },
}
