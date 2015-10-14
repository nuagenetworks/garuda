# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin

class GAChannel(GAPlugin):
    """
    """
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

    def set_core_controller(self, core_controller):
        """
        """
        raise NotImplemented('Channel must implement set_core_controller method')
