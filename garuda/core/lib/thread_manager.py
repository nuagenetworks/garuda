# -*- coding: utf-8 -*-

import threading
from functools import partial
from multiprocessing.pool import ThreadPool


class ThreadManager(object):
    """ Multi thread manager

    """
    def __init__(self, size=20):
        """ Initializes a ThreadManager

        """
        self._size = size
        self._pool = None

    def callback(self, result):
        """
        """
        print "callback in %s" % self
        print result

    def start(self, method, elements, async=False, callback=None, *args, **kwargs):
        """ Start a method in a separate process

            Args:
                method: the method to start in a separate process
                args: Accept args/kwargs arguments
        """
        self._pool = ThreadPool(self._size)

        partial_method = partial(method, *args, **kwargs)

        print '%s > ASYNC = %s'  % (self, async)

        if async is False:
            results = self._pool.map(partial_method, elements)
            self._pool.close()
            self._pool.join()
            return results

        if callback is None:
            callback = self.callback

        return self._pool.map_async(partial_method, elements, callback=callback)

    def stop_all(self):
        """ Stop all current processes
        """
        self._pool.terminate()
