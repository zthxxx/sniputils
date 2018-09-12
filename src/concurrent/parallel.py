import os
from queue import Queue
from threading import Event, Thread


class ActorExitException(Exception):
    pass


class Parallel(object):
    """
    Actor model
    https://en.wikipedia.org/wiki/Actor_model

    Usage:
        import time
        from random import randint

        def func(param):
            time.sleep(randint(2, 3))
            print('param:', param)

        poi =  Parallel(func)
        poi.put(1)
        poi.put(3)
        poi.run_as_async()
        poi.puts([5, 7, 9])
        # output rand ->
        # get param 1
        # get param 5
        # ...
        # get param 7

        # if await with keep flag
        poi.await(keep=True) # -> will block because the `keep` flag set will block until self.stop()
                             # its exit with poi.stop() in another thread
        # else if only use await
        poi.await() # -> will block until tasks consumed finish

        -----

        poi =  Parallel(func)
        poi.puts([1, 2, 3])
        poi.run_as_async()
        print('start')
        poi.await()
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3
        # end

        -----

        poi =  Parallel(func)
        poi.puts([1, 2, 3])
        poi.run_as_await()
        print('start')
        poi.put(None)

        # output ->
        # param: 2
        # param: 1
        # param: 3
        # start
        # raise ActorExitException: This actor is terminated

        -----

        poi =  Parallel(func)
        poi.run_as_async()
        print('start')
        poi.puts([1, 2, 3])

        # output raise ->
        # ActorExitException: This actor is terminated

        -----

        poi =  Parallel(func, keep=True)
        poi.run_as_async()
        print('start')
        poi.puts([1, 2, 3])
        poi.await()
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3  <- blocked in here until poi.stop()

        -----

        poi =  Parallel(func, preload=[1, 2, 3])
        # equal Parallel(func).puts([1, 2, 3])

    """
    def __init__(self, func, preload: list=None, keep=False, size=os.cpu_count()):
        self.method = func
        self.keep = keep
        self.size = size
        self.queue = Queue(maxsize=size)
        self.tasks = []
        self._event = None
        for item in preload or []:
            self.queue.put(item)

    def put(self, item):
        if self.is_stop():
            raise ActorExitException('This actor is terminated')
        self.queue.put(item)

    def puts(self, items):
        for item in items:
            self.put(item)

    def _consumer(self):
        while True:
            if not self.keep and self.queue.empty():
                raise ActorExitException()
            item = self.queue.get()
            if item is ActorExitException:
                raise ActorExitException()
            self.method(item)

    def _bootstrap(self):
        try:
            self._consumer()
        except ActorExitException:
            pass
        finally:
            self._event.set()

    def is_stop(self):
        return bool(self._event and self._event.is_set())

    def run_as_async(self):
        if self._event is not None:
            if self.is_stop():
                raise ActorExitException('This actor is terminated')
            return
        self._event = Event()
        for index in range(self.size):
            task = Thread(name='parallel', target=self._bootstrap)
            self.tasks.append(task)
            task.start()

    def run_as_await(self):
        self.run_as_async()
        self.await()

    def await(self, keep=False):
        self.keep = self.keep or keep
        for task in self.tasks:
            task.join()
        while not self.queue.empty():
            self.queue.get_nowait()
        self.queue.task_done()

    def stop(self):
        self.keep = False
        self.put(ActorExitException)
        self.await()
