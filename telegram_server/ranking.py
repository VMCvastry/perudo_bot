from collections import Counter

from bots import get_sandbox_bot
from bots.bot_class import Bot
from database import Database
from perudo_game.game_core import Game
from perudo_game.players import PlayerInterface
from perudo_game.ui.no_ui import NoUI


def find_winner(players, ui):
    results = [Game(players, ui).start() for _ in range(50)]
    print(results)
    print(Counter(results))
    winner = Counter(results).most_common(1)[0][0]
    return winner


def rank_and_save_bot(bot: Bot, db_path):
    db = Database(db_path)
    bots = db.get_all_bots()
    victory = 0
    defeat = 0
    player = get_sandbox_bot(bot)
    for enemy in bots:
        ui = NoUI()
        players = {
            0: get_sandbox_bot(enemy)(0),
            1: player(1),
        }
        winner = find_winner(players, ui)
        if not winner:
            defeat += 1
            db.add_victory(enemy.bot_id)
        else:
            victory += 1
            db.add_defeat(enemy.bot_id)
    bot.victory = victory
    bot.defeat = defeat
    db.add_bot(bot)
    return bot.get_win_ratio()
