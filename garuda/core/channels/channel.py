# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from garuda.core.models import GAPlugin

class GAChannel(GAPlugin):
    """
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def channel_type(self):
        """
        """
        pass

    @abstractmethod
    def start(self):
        """
        """
        pass

    @abstractmethod
    def stop(self):
        """
        """
        pass

    @abstractmethod
    def is_running(self):
        """
        """
        pass

    @abstractmethod
    def receive(self):
        """
        """
        pass

    @abstractmethod
    def send(self):
        """
        """
        pass

    @abstractmethod
    def push(self):
        """
        """
        pass
