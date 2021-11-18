import traceback

from .bot_class import Bot
from perudo_game.players import PlayerInterface
from database import Database
from bots import get_sandbox_bot


def test_new_bot(player: PlayerInterface):
    return True


def get_new_bot(user_id, code) -> Bot:
    bot = Bot(None, None, user_id, code)
    try:
        player = get_sandbox_bot(bot)
        test_new_bot(player)
        bot.name = player.get_player_name()
    except Exception as e:
        traceback.print_exc()
    return bot


def test_and_save_new_bot(db: Database, user_id, code):
    bot = get_new_bot(user_id, code)
    if bot:
        db.add_bot(bot)
        return True
    return False
