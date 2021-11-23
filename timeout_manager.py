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
    # time.sleep(5)
    queue.put(function(*args))


def execute_with_timeout(function, args: tuple, timeout=3):
    q = Queue()
    p1 = Process(
        target=process_returner,
        args=(q, function, args),
        name="Process_inc_forever",
    )
    p1.start()
    p1.join(timeout=timeout)
    p1.terminate()
    print(p1)
    print(p1.exitcode)
    if p1.exitcode is None:
        print(f"Oops, {p1} timeouts!")
        raise TimeoutError
    return q.get()
    # return q.get() if not q.empty() else None
