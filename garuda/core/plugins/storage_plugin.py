# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from garuda.core.models import GAPlugin

class GAStoragePlugin(GAPlugin):
    """
    """

    __metaclass__ = ABCMeta

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    @abstractmethod
    def instantiate(self, resource_name):
        """
        """
        pass

    @abstractmethod
    def get(self, resource_name, identifier):
        """
        """
        pass

    @abstractmethod
    def get_all(self, parent, resource_name):
        """
        """
        pass

    @abstractmethod
    def save(self, resource, parent=None):
        """
        """
        pass

    @abstractmethod
    def delete(self, resource, cascade=True):
        """
        """
        pass
