import traceback

from .bot_class import Bot
from perudo_game.players import PlayerInterface
from database import Database
from bots import get_sandbox_bot


def test_new_bot(player: type[PlayerInterface]):
    return True


def remove_imports(text):
    text = text.splitlines()
    for line in text:
        if "import" in line:
            text.remove(line)
    return "\n".join(text)


def get_new_bot(user_id, code) -> (Bot, type[PlayerInterface]):
    bot = Bot(None, None, user_id, remove_imports(code))
    try:
        player = get_sandbox_bot(bot)
        test_new_bot(player)
        bot.name = player.get_player_name()
        return bot
    except Exception as e:
        traceback.print_exc()


# def test_and_save_new_bot(db: Database, user_id, code):
#     bot = get_new_bot(user_id, code)
#     if bot:
#         db.add_bot(bot)
#         return True
#     return False
