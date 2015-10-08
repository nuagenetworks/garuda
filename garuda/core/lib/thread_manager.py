# -*- coding: utf-8 -*-

import threading


class StoppableThread(threading.Thread):
    """
    """

    def __init__(self, *args, **kwargs):
        """
        """
        super(StoppableThread, self).__init__(*args, **kwargs)

    def stop(self):
        """
        """
        self._Thread__stop()  # This is a fucking hack, but it works ! (08/27/2015)


class ThreadManager(object):
    """ Multi thread manager

    """
    def __init__(self):
        """ Initializes a ThreadManager

        """
        self._threads = list()

    def wait_until_exit(self):
        """ Wait until all process are finished.

        """
        for thread in self._threads:
            thread.join(timeout=1)

        self._threads = list()

    def start(self, method, *args, **kwargs):
        """ Start a method in a separate process

            Args:
                method: the method to start in a separate process
                args: Accept args/kwargs arguments
        """
        thread = StoppableThread(target=method, args=args, kwargs=kwargs)
        thread.is_daemon = True
        thread.name = method
        thread.start()
        self._threads.append(thread)

    def is_running(self):
        """ Returns true if one process is running
        """
        for thread in self._threads:
            if thread.is_alive():
                return True

        return False

    def stop_all(self):
        """ Stop all current processes
        """
        for thread in self._threads:
            thread.stop()

        self.wait_until_exit()
