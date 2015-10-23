# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin


class GAPermissionsPlugin(GAPlugin):
    """
    """

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def create_permission(self, resource, target, action, implicit=False):
        """
        """
        raise NotImplementedErrorError("%s should implement create_permission method" % self)

    def remove_permission(self, resource, target, action):
        """
        """
        raise NotImplementedErrorError("%s should implement remove_permission method" % self)

    def has_permission(self, resource, target, action):
        """
        """
        raise NotImplementedErrorError("%s should implement has_permission method" % self)
