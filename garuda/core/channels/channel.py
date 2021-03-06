# -*- coding: utf-8 -*-
import time
import signal
import sys


class GAChannel(object):
    """
    """

    def __init__(self):  # pragma: no cover
        """
        """
        self._core_controller = None

    @classmethod
    def manifest(cls):  # pragma: no cover
        """
        """
        raise NotImplementedError('manifest method must be implemented')

    @property
    def core_controller(self):  # pragma: no cover
        """
        """
        return self._core_controller

    @core_controller.setter
    def core_controller(self, core_controller):  # pragma: no cover
        """
        """
        self._core_controller = core_controller

    def channel_type(self):  # pragma: no cover
        """
        """
        raise NotImplementedError('Channel must implement channel_type method')

    def run(self):  # pragma: no cover
        """
        """
        raise NotImplementedError('Channel must implement start method')

    def receive(self):  # pragma: no cover
        """
        """
        raise NotImplementedError('Channel must implement receive method')

    def send(self):  # pragma: no cover
        """
        """
        raise NotImplementedError('Channel must implement send method')

    def push(self):  # pragma: no cover
        """
        """
        raise NotImplementedError('Channel must implement push method')

    def did_fork(self):  # pragma: no cover
        """
        """
        pass

    def will_exit(self):  # pragma: no cover
        """
        """
        pass

    def did_exit(self):  # pragma: no cover
        """
        """
        pass

    def start_runloop(self):  # pragma: no cover
        """
        """
        def handle_signal(signal_number, frame_stack):
            self.will_exit()
            sys.exit(0)

        signal.signal(signal.SIGTERM, handle_signal)

        while True:
            time.sleep(30000)
