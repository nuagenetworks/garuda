# -*- coding: utf-8 -*-

from .abstracts import GAPlugin
from garuda.core.exceptions import NotImplementedException

class GACommunicationChannel(GAPlugin):
    """

    """

    CHANNEL_TYPE_REST = 0
    CHANNEL_TYPE_XMPP = 1
    CHANNEL_TYPE_OTHER = 2

    def channel_type(self):
        """
        """
        raise NotImplementedException('CommunicationChannel should implement channel_type method')

    def start(self):
        """
        """
        raise NotImplementedException('CommunicationChannel should implement start method')

    def stop(self):
        """
        """
        raise NotImplementedException('CommunicationChannel should implement stop method')

    def is_running(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement is running method')

    def receive(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement receive method')

    def send(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement send method')

    def push(self):
        """

        """
        raise NotImplementedException('CommunicationChannel should implement push method')
