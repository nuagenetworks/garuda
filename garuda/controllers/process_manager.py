# -*- coding: utf-8 -*-

from multiprocessing import Process


class ProcessManager(object):
    """ Multi process manager

    """
    def __init__(self):
        """ Initializes a ProcessManager

        """
        self._processes = list()

    def wait_until_exit(self):
        """ Wait until all process are finished.

        """
        [t.join() for t in self._processes]

        self._processes = list()

    def start(self, method, *args, **kwargs):
        """ Start a method in a separate process

            Args:
                method: the method to start in a separate process
                args: Accept args/kwargs arguments
        """
        process = Process(target=method, args=args, kwargs=kwargs)
        process.is_daemon = True
        process.start()
        self._processes.append(process)

    def is_running(self):
        """ Returns true if one process is running
        """

        for process in self._processes:
            if process.is_alive():
                return True

        return False

    def stop_all(self):
        """ Stop all current processes
        """
        for process in self._processes:
            process.terminate()

        self.wait_until_exit()
