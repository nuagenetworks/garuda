# -*- coding: utf-8 -*-

import threading
from functools import partial
from multiprocessing.pool import ThreadPool


class StoppableThread(threading.Thread):
    """
    """

    def __init__(self, *args, **kwargs):
        """
        """
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.__value = None

    def stop(self):
        """
        """
        self._Thread__stop()


class ThreadManager(object):
    """ Multi thread manager

    """
    def __init__(self, size=20):
        """ Initializes a ThreadManager

        """
        self._size = size
        self._pool = None

    @classmethod
    def start_thread(self, method, *args, **kwargs):
        """
        """
        thread = StoppableThread(target=method, args=args, kwargs=kwargs)
        thread.is_daemon = True
        thread.name = method
        thread.start()
        return thread

    @classmethod
    def stop_thread(self, thread):
        """
        """
        thread.stop()
        thread.join(timeout=1)

    def start(self, method, elements, async=False, callback=None, *args, **kwargs):
        """
        """
        self._pool = ThreadPool(self._size)

        partial_method = partial(method, *args, **kwargs)

        if async is False:
            results = self._pool.map(partial_method, elements)
            self._pool.close()
            self._pool.join()
            return results

        return self._pool.map_async(partial_method, elements, callback=callback)

    def stop_all(self):
        """
        """
        self._pool.terminate()
