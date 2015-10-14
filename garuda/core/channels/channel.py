# -*- coding: utf-8 -*-
import time
import signal
import sys

from garuda.core.models import GAPlugin

class GAChannel(object):
    """
    """

    def __init__(self):
        """
        """
        self._core_controller = None

    @classmethod
    def manifest(cls):
        """
        """
        raise NotImplemented("manifest method must be implemented")

    @property
    def core_controller(self):
        """
        """
        return self._core_controller

    @core_controller.setter
    def core_controller(self, core_controller):
        """
        """
        self._core_controller = core_controller

    def channel_type(self):
        """
        """
        raise NotImplemented('Channel must implement channel_type method')

    def run(self):
        """
        """
        raise NotImplemented('Channel must implement start method')

    def receive(self):
        """
        """
        raise NotImplemented('Channel must implement receive method')

    def send(self):
        """
        """
        raise NotImplemented('Channel must implement send method')

    def push(self):
        """
        """
        raise NotImplemented('Channel must implement push method')

    def did_fork(self):
        """
        """
        pass

    def will_exit(self):
        """
        """
        pass

    def did_exit(self):
        """
        """
        pass

    def start_runloop(self):
        """
        """
        def handle_signal(signal_number, frame_stack):
            self.will_exit()
            sys.exit(0)

        signal.signal(signal.SIGTERM, handle_signal)

        while True:
            time.sleep(30000)
