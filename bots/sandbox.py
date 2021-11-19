from bots.bot_class import Bot
from perudo_game.players import PlayerInterface
from perudo_game.game.gameMove import GameMove
from perudo_game.game.game_info import GameInfo
import random
from collections import Counter


def get_sandbox_bot(bot: Bot) -> PlayerInterface:
    global_scope = {"__builtins__": __builtins__.copy()}
    # print(global_scope["__builtins__"])
    del global_scope["__builtins__"]["print"]
    # print(PlayerInterface.__dict__)
    local_scope = {
        "GameInfo": GameInfo,
        "PlayerInterface": PlayerInterface,
        "GameMove": GameMove,
        "Counter": Counter,
        "random": random,
    }
    exec(bot.code, global_scope, local_scope)
    # print(global_scope, local_scope)
    print(local_scope)
    # a = local_scope["Bot1"](1)
    # print(a.get_player_name())
    return local_scope["Bot1"]
