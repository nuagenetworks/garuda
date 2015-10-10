# -*- coding: utf-8 -*-

from .plugin import GAPlugin

class GACommunicationChannel(GAPlugin):
    """

    """

    CHANNEL_TYPE_REST = 0
    CHANNEL_TYPE_XMPP = 1
    CHANNEL_TYPE_OTHER = 2

    def channel_type(self):
        """
        """
        raise NotImplemented('CommunicationChannel should implement channel_type method')

    def start(self):
        """
        """
        raise NotImplemented('CommunicationChannel should implement start method')

    def stop(self):
        """
        """
        raise NotImplemented('CommunicationChannel should implement stop method')

    def is_running(self):
        """

        """
        raise NotImplemented('CommunicationChannel should implement is running method')

    def receive(self):
        """

        """
        raise NotImplemented('CommunicationChannel should implement receive method')

    def send(self):
        """

        """
        raise NotImplemented('CommunicationChannel should implement send method')

    def push(self):
        """

        """
        raise NotImplemented('CommunicationChannel should implement push method')
