from database import Database
from bots.sandbox import get_sandbox_bot


def read_file(path) -> str:
    with open(path, "r") as f:
        return f.read()


db = Database("./bots.db")
# bot = read_bot_file("code.txt")
# a = db.add_bot(bot)
# print(a)
bot = db.get_bot(6)
get_sandbox_bot(bot)
