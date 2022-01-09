# import signal
# from contextlib import contextmanager
#
#
# @contextmanager
# def timeout(time):
#     signal.signal(signal.SIGALRM, raise_timeout)
#     signal.alarm(time)
#     try:
#         yield
#     except TimeoutError:
#         print("Time out Error")
#         raise TimeoutError
#
#     finally:
#         signal.signal(signal.SIGALRM, signal.SIG_IGN)
#
#
# def raise_timeout(signum, frame):
#     raise TimeoutError
import time
from multiprocessing import Process, Queue
from threading import Thread


def process_returner(queue, function, args):
    queue.put(function(*args))


def execute_with_timeout(function, args: tuple, timeout=3):
    q = Queue()
    p1 = Process(
        target=process_returner,
        args=(q, function, args),
        name="P",
    )
    p1.start()
    time.sleep(0.001)
    p1.join(timeout=timeout)
    if p1.exitcode is None:
        time.sleep(1)
        if p1.exitcode is None:
            # print(f"Oops, {p1} timeouts!")
            p1.terminate()
            raise TimeoutError("Timeout Error, Move took too long")
    p1.terminate()
    return q.get() if not q.empty() else None
