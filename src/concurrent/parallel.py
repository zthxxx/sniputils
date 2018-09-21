import os
from queue import Queue
from threading import Barrier, Event, Thread
from typing import Callable, Generator, Iterable


class ActorExitException(Exception):
    pass


class Parallel(object):
    """
    Actor model extension

    https://en.wikipedia.org/wiki/Actor_model

    Usage:

    .. code:: python

        # global define in those case
        import time
        from random import randint

        def func(param):
            time.sleep(randint(1, 2))
            print('param:', param)
            return param

    .. code:: python

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

        # if await with `keep` flag
        poi.await_at(keep=True) # -> will block because the `keep` flag set will block until self.stop()
                             # its exit with poi.stop() in another thread
        # else if only use await
        poi.await_at() # -> will block until tasks were consumed finish

    .. code:: python

        # if want to block put, set `queue.maxsize`

        poi.queue.maxsize = poi.size

    .. code:: python

        poi =  Parallel(func)
        poi.puts([1, 2, 3])
        poi.run_as_async()
        print('start')
        poi.await_at()
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3
        # end

    .. code:: python

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

    .. code:: python

        poi =  Parallel(func)
        poi.run_as_async()
        print('start')
        poi.puts([1, 2, 3])

        # output raise ->
        # ActorExitException: This actor is terminated

    .. code:: python

        poi =  Parallel(func, keep=True)
        poi.run_as_async()
        print('start')
        poi.puts([1, 2, 3])
        poi.await_at()
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3  <- blocked in here until poi.stop()

    .. code:: python

        poi =  Parallel(func, keep=True)
        poi.run_as_async()
        print('start')
        poi.puts([1, 2, 3])
        time.sleep(3)
        print('sleep timeout')
        poi.await_at(keep=False)
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3
        # sleep timeout
        # end

    .. code:: python

        poi =  Parallel(func, preload=[1, 2, 3])
        print('start')
        poi.run_as_async()
        time.sleep(3)
        print('sleep timeout')
        poi.await_at(keep=True)
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3
        # sleep timeout
        # end

    .. code:: python

        poi =  Parallel(func, preload=[1, 2, 3])
        print('start')
        poi.run_as_async()
        poi.await_at(keep=True)
        print('end')

        # output ->
        # start
        # param: 2
        # param: 1
        # param: 3 <- blocked in here until poi.stop()

    .. code:: python

        poi =  Parallel(func, preload=[1, 2, 3])
        ...
        # equal Parallel(func).puts([1, 2, 3])

    .. code:: python

        poi =  Parallel(func, preload=[1, 2, 3])
        poi.run_as_async()
        results = list(poi.results)
        print('results', results)
        for item in poi.results:
            print('item', item)
        print('tasks end')

        # output ->
        # results [2, 1, 3]
        # tasks end

    .. code:: python

        poi =  Parallel(func, preload=[1, 2, 3])
        poi.run_as_async()
        for item in poi.results:
            print('item', item)
        print('tasks end')

        # output ->
        # item 2
        # item 1
        # item 3
        # tasks end

    """

    def __init__(self, func: Callable[[any], any], preload: Iterable = None, keep=False, size=os.cpu_count()):
        """
        parallel run func with multi-threading

        :param func: target method to run, need receive an arg
        :param preload: preload any args
        :param keep: whether or not keep thread while queue is empty
                     if keep=False, thread will auto close while task end
        :param size: how much thread to parallel run
        """
        self.method = func
        self.keep = keep
        self.size = size
        self.queue = Queue()
        self.tasks = []

        self._is_start = Event()
        self._is_stop = Event()

        self.callbacks = [self._tasks_done_notify]
        self._tasks_done = Barrier(size, action=self._tasks_done_callback)

        self._results = Queue()
        self._results_gen = None

        for item in preload or []:
            self.queue.put(item)

    def put(self, item):
        if self.is_stop:
            raise ActorExitException('This actor is terminated')
        self.queue.put(item)

    def puts(self, items):
        for item in items:
            self.put(item)

    def _consumer(self):
        while True:
            if not self.keep and self.queue.empty():
                raise ActorExitException
            item = self.queue.get()
            self.queue.task_done()
            if item is ActorExitException:
                raise ActorExitException
            result = self.method(item)
            if result is not None:
                self._results.put(result)

    def _bootstrap(self):
        try:
            self._consumer()
        except ActorExitException:
            pass
        finally:
            if not self.keep and self.queue.empty():
                self.put(ActorExitException)
            self._tasks_done.wait()

    def _tasks_done_callback(self):
        self._is_stop.set()
        for callback in self.callbacks:
            if not isinstance(callback, Callable):
                continue
            callback()

    def _tasks_done_notify(self):
        self._results.put(ActorExitException)

    def _get_result(self):
        while True:
            result = self._results.get()
            self._results.task_done()
            if result is ActorExitException:
                return
            yield result

    @property
    def results(self) -> Generator:
        if not self._results_gen:
            self._results_gen = self._get_result()
        return self._results_gen

    @property
    def is_stop(self):
        return self._is_stop.is_set()

    @property
    def is_start(self):
        return self._is_start.is_set()

    def run_as_async(self):
        if self.is_stop:
            raise ActorExitException('This actor is terminated')
        if self.is_start:
            return self
        self._is_start.set()
        for index in range(self.size):
            task = Thread(name='parallel', target=self._bootstrap)
            self.tasks.append(task)
            task.start()
        return self

    def run_as_await(self):
        self.run_as_async()
        return self.await_at()

    def await_at(self, keep: bool = None):
        if isinstance(keep, bool):
            if self.keep and not keep:
                self.puts([ActorExitException] * self.size)
            self.keep = keep
        for task in self.tasks:
            task.join()
        self._is_stop.set()
        while not self.queue.empty():
            self.queue.get_nowait()
            self.queue.task_done()
        return self.results

    def stop(self):
        return self.await_at(keep=False)

    def __call__(self, arg_iter: Iterable=None):
        self.keep = True
        self.run_as_async()
        self.puts(arg_iter or [])
        return self.stop()
