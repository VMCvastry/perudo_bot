import traceback

from .bot_class import Bot
from perudo_game.players import PlayerInterface
from database import Database
from bots import get_sandbox_bot
from bots.test_player import TestBot


def remove_imports(text):
    text = text.splitlines()
    for i, line in enumerate(text):
        if "import" in line:
            text[i] = " "
    return "\n".join(text)


def get_new_bot(user_id, code) -> (Bot, type[PlayerInterface]):
    bot = Bot(None, None, user_id, remove_imports(code))
    player = get_sandbox_bot(bot)
    TestBot(player).test()
    bot.name = player.get_player_name()
    return bot


# def test_and_save_new_bot(db: Database, user_id, code):
#     bot = get_new_bot(user_id, code)
#     if bot:
#         db.add_bot(bot)
#         return True
#     return False
