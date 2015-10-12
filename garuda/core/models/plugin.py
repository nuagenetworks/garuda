# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class GAPlugin(object):
    """
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """
        """
        self.core_controller = None

    def will_register(self):
        """
        """
        pass

    def did_register(self):
        """
        """
        pass

    def will_unregister(self):
        """
        """
        pass

    def did_unregister(self):
        """
        """
        pass

    @classmethod
    @abstractmethod
    def manifest(cls):
        """
        """
        raise NotImplemented("manifest method must be implemented")