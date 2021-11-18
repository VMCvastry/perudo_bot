from bots.sandbox import get_sandbox_bot
from database import Database
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
#
# logger.setLevel(logging.DEBUG)


def read_file(path) -> str:
    with open(path, "r") as f:
        return f.read()


db = Database("./bots.db")
# bot = read_bot_file("code.txt")
# a = db.add_bot(bot)
# print(a)
bot = db.get_bot(1)
get_sandbox_bot(bot)
