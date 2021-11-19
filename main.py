from bots.add_new_bot import get_new_bot
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


# def read_file(path) -> str:
#     with open(path, "r") as f:
#         return f.read()
#
#
db = Database("./bots.db")
# # bot = read_bot_file("code.txt")
# # a = db.add_bot(bot)
# # print(a)
# bot = db.get_bot(1)
# get_sandbox_bot(bot)

# with open("./test.py", "r") as f:
#     get_new_bot(0, f.read())
get_sandbox_bot(db.get_bot(4))(1)
