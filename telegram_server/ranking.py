from collections import Counter
from multiprocessing import Process, Array

from bots import get_sandbox_bot
from bots.bot_class import Bot
from database import Database
from perudo_game.exceptions import PlayerException
from perudo_game.game_core import Game


def play_game(players, results, i):
    try:
        results[i] = Game(players).start()
    except PlayerException as e:
        results[i] = -1
        print(e)
    return


def find_winner(players):
    n_games = 25
    results = Array("i", [-1] * n_games)
    threads = set()
    for i in range(n_games):
        t = Process(target=play_game, args=(players, results, i))
        threads.add(t)
        t.start()
    for t in threads:
        t.join()
        t.terminate()
    results = list(results)
    # print(results)
    print(Counter(results))
    winner = Counter(results).most_common(1)[0][0]
    return winner


def rank_and_save_bot(bot: Bot, update_to_user):
    db = Database()
    bots = db.get_leaderboard()
    victory = 0
    defeat = 0
    exception = 0
    player = get_sandbox_bot(bot)
    for enemy in bots:
        players = {
            0: get_sandbox_bot(enemy),
            1: player,
        }
        winner = find_winner(players)
        if not winner:
            defeat += 1
            db.add_victory(enemy.bot_id)
            update_to_user(f"You lost against {enemy}")
        elif winner == 1:
            victory += 1
            db.add_defeat(enemy.bot_id)
            update_to_user(f"You won against {enemy}")
        elif winner == -1:
            exception += 1
            update_to_user(f"Many Errors when playing with {enemy}")
            # db.add_exception(enemy.bot_id)
    bot.victory = victory
    bot.defeat = defeat
    db.add_bot(bot)
    update_to_user(str(bot.get_win_ratio() * 100) + "% victories")
