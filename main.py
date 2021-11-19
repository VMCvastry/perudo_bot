import time

from bots.add_new_bot import get_new_bot
from bots.sandbox import get_sandbox_bot
from database import Database
import logging

from perudo_game.game.game_info import GameInfo
from timeout_manager import execute_with_timeout

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
#
# logger.setLevel(logging.DEBUG)

db = Database("./bots.db")
status = GameInfo([], 0, [[]], True)
b = get_sandbox_bot(db.get_bot(4))(1)
b.set_rolled_dices([1, 2, 3])
execute_with_timeout(b.set_rolled_dices, ([5, 6, 7],), timeout=3)
print(b.numbers)
# f = b.make_a_move
# print(execute_with_timeout(f, (status,), timeout=3))
from threading import Thread

#
#
# def a():
#     print("hi")
#     # return 3
#     while 1:
#         pass
#
#
# def wrapper(l, a):
#     l.append(a())
#     print(l)
#
#
# L = ["a"]
# p1 = Thread(target=wrapper, args=(L, a), name="Process_inc_forever")
# p1.start()
#
# p1.join(timeout=3)

# p1.
# print(p1)
# print(p1.exitcode)
# if p1.exitcode is None:
#     print(f"Oops, {p1} timeouts!")

# def read_file(path) -> str:
#     with open(path, "r") as f:
#         return f.read()
#
#
# # bot = read_bot_file("code.txt")
# # a = db.add_bot(bot)
# # print(a)
# bot = db.get_bot(1)
# get_sandbox_bot(bot)
# def saver(q, f, args):
#     time.sleep(5)
#     q.put(f(*args))
#
#
# Q = Queue()
# status = GameInfo([], 0, [[]], True)
# b = get_sandbox_bot(db.get_bot(4))(1)
# b.set_rolled_dices([1, 2, 3])
# p1 = Process(
#     target=saver,
#     args=(Q, b.make_a_move, (status,)),
#     name="Process_inc_forever",
# )
# p1.start()
# p1.join(timeout=3)
# p1.terminate()
# print(p1)
# print(p1.exitcode)
# if p1.exitcode is None:
#     print(f"Oops, {p1} timeouts!")
# print(Q.get())
# with open("./test.py", "r") as f:
#     get_new_bot(0, f.read())
# status = None
# try:
#     with timeout(2):
#         print("entering block")
#         import time
#
#         time.sleep(10)
#
#         b = get_sandbox_bot(db.get_bot(4))(1)
#         b.make_a_move(status)
#         print("This should never get printed because the line before timed out")
# except TimeoutError as e:
#     print("csas")
#     print(e)
# # print("pizza")
