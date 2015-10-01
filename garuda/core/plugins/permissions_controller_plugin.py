# -*- coding: utf-8 -*-

from .abstracts import GAPlugin


class GAPermissionsControllerPlugin(GAPlugin):
    """
    """
    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def create_permission(self, resource, target, action, implicit=False):
        """
        """
        raise NotImplementedError("%s should implement create_permission method" % self)

    def remove_permission(self, resource, target, action):
        """
        """
        raise NotImplementedError("%s should implement remove_permission method" % self)

    def has_permission(self, resource, target, action):
        """
        """
        raise NotImplementedError("%s should implement has_permission method" % self)
