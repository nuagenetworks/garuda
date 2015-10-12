# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from garuda.core.models import GAPlugin

class GAPermissionsPlugin(GAPlugin):
    """
    """

    __metaclass__ = ABCMeta

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    @abstractmethod
    def create_permission(self, resource, target, action, implicit=False):
        """
        """
        pass

    @abstractmethod
    def remove_permission(self, resource, target, action):
        """
        """
        pass

    @abstractmethod
    def has_permission(self, resource, target, action):
        """
        """
        pass
