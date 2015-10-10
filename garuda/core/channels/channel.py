# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin

class GAChannel(GAPlugin):
    """
    """

    def channel_type(self):
        """
        """
        raise NotImplemented('Channel must implement channel_type method')

    def start(self):
        """
        """
        raise NotImplemented('Channel must implement start method')

    def stop(self):
        """
        """
        raise NotImplemented('Channel must implement stop method')

    def is_running(self):
        """
        """
        raise NotImplemented('Channel must implement is running method')

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
