import time
from collections import Counter
from threading import Thread

from bots import get_sandbox_bot
from bots.bot_class import Bot
from database import Database
from perudo_game.exceptions import PlayerException
from perudo_game.game_core import Game
from perudo_game.players import PlayerInterface
from perudo_game.ui.no_ui import NoUI


def play_game(players, ui, results, i):
    try:
        results[i] = Game(players, ui).start()
    except PlayerException as e:
        results[i] = -1
        print(e)
    return


def find_winner(players, ui):
    n = 25
    results = [-1] * n
    threads = set()
    for i in range(n):
        # play_game(players, ui, results, i)
        t = Thread(target=play_game, args=(players, ui, results, i))
        threads.add(t)
        t.start()
        time.sleep(0.001)
    for t in threads:
        t.join()
    print(results)
    print(Counter(results))
    winner = Counter(results).most_common(1)[0][0]
    return winner


def rank_and_save_bot(bot: Bot):
    db = Database()
    bots = db.get_all_bots()
    victory = 0
    defeat = 0
    exception = 0
    player = get_sandbox_bot(bot)
    for enemy in bots:
        ui = NoUI()
        players = {
            0: get_sandbox_bot(enemy),
            1: player,
        }
        winner = find_winner(players, ui)
        if not winner:
            defeat += 1
            db.add_victory(enemy.bot_id)
        elif winner == 1:
            victory += 1
            db.add_defeat(enemy.bot_id)
        elif winner == -1:
            exception += 1
            # db.add_exception(enemy.bot_id)
    bot.victory = victory
    bot.defeat = defeat
    db.add_bot(bot)
    return bot.get_win_ratio()
