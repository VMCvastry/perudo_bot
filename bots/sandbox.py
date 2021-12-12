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
    # print(global_scope["__builtins__"])
    for f in removed_functions:
        del global_scope["__builtins__"][f]
    # print(PlayerInterface.__dict__)
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
    exec(bot.code, global_scope, local_scope)
    # print(global_scope, local_scope)
    # print(local_scope)
    # a = local_scope["Bot1"](1)
    # print(a.get_player_name())
    if "Player" not in local_scope:
        raise TestNotPassedException("No 'class Player()' definition")
    return local_scope["Player"]
