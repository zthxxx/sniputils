import os
from queue import Queue
from threading import Thread


# end with None in get()
def consumer(queue, method):
    while True:
        item = queue.get()
        if item is None:
            queue.put(None)
            queue.task_done()
            break
        method(item)


def producer(queue, item):
    queue.put(item)


def parallel(method, size=os.cpu_count()):
    q = Queue(maxsize=size)
    tasks = []
    for index in range(size):
        task = Thread(name='parallel', target=consumer, args=(q, method))
        tasks.append(task)
        task.start()
    return tasks, lambda item: producer(q, item)
