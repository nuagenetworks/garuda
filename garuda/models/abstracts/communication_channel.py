# -*- coding: utf-8 -*-

from garuda.exceptions import NotImplementedException


class CommunicationChannel(object):
    """

    """
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
