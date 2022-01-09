import itertools
import math

from bots.bot_class import Bot
from perudo_game.players import PlayerInterface
from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
import random, json
from collections import Counter
from bots.test_player import TestNotPassedException

removed_functions = ["print", "eval", "exec"]


def get_sandbox_bot(bot: Bot) -> type[PlayerInterface]:
    global_scope = {"__builtins__": __builtins__.copy()}
    for f in removed_functions:
        del global_scope["__builtins__"][f]
    local_scope = {
        "GameInfo": GameInfo,
        "PlayerInterface": PlayerInterface,
        "GameMove": GameMove,
        "Counter": Counter,
        "random": random,
        "json": json,
        "math": math,
        "itertools": itertools,
    }
    global_scope.update(local_scope)
    try:
        exec(bot.code, global_scope, local_scope)
    except Exception as e:
        raise TestNotPassedException(f"Syntax error:\n{e}")
    if "Player" not in local_scope:
        raise TestNotPassedException("No 'class Player()' definition")
    return local_scope["Player"]
