# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin


class GAPermissionsPlugin(GAPlugin):
    """
    """

    def should_manage(self, resource_name, identifier):  # pragma: no cover
        """
        """
        return True

    def interpret_permissions(self, todo):  # pragma: no cover
        """
        """
        raise NotImplementedError("%s should implement create_permission method" % self)
