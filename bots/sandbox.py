from bots.bot_class import Bot
from perudo_game.players import PlayerInterface


def get_sandbox_bot(bot: Bot) -> PlayerInterface:
    global_scope = {"__builtins__": __builtins__.__dict__.copy()}
    # print(global_scope["__builtins__"])
    del global_scope["__builtins__"]["print"]
    # print(PlayerInterface.__dict__)
    local_scope = {"PlayerInterface": PlayerInterface}
    exec(bot.code, global_scope, local_scope)
    # print(global_scope, local_scope)
    print(local_scope)
    a = local_scope["Bot1"](1)
    print(a.get_player_name())
    return a
