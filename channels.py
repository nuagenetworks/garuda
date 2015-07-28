# -*- coding: utf-8 -*-

from gaexceptions import NotImplementedException


class CommunicationChannel(object):
    """

    """
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