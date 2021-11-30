from telegram_server.human_player_logic.human_showdown import showdown_handler
from telegram_server.telegram_commands import *
from telegram_server.user_setup import user_setup_handler
from telegram_server.upload_bot import upload_bot
import os
from telegram.ext import (
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


# logging.basicConfig(
#     level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )


def main():
    try:
        token = os.environ["telegram_token"]
    except KeyError:
        from telegram_server.telegram_token import token
    port = int(os.environ.get("PORT", 80))
    updater = Updater(token=token, arbitrary_callback_data=True)

    dispatcher = updater.dispatcher
    handlers = [
        user_setup_handler,
        showdown_handler,
        CommandHandler("leaderboard", get_leaderboard),
        MessageHandler(Filters.text & (~Filters.command), echo),
        # CallbackQueryHandler(callback),
        MessageHandler(Filters.document, upload_bot),
    ]
    # upload_handler = CommandHandler("upload", upload_bot)
    for h in handlers:
        dispatcher.add_handler(h)
    try:
        token = os.environ["telegram_token"]
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(port),
            url_path=token,
            webhook_url="https://perudo-arena-bot.herokuapp.com/" + token,
        )
    except KeyError:
        updater.start_polling()
