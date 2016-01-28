# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin


class GAPermissionsPlugin(GAPlugin):
    """
    """

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def create_permission(self, resource, target, permission, explicit=True, parent_permission_id=None):
        """
        """
        raise NotImplementedError("%s must implement create_permission method" % self)

    def remove_permission(self, resource, target, permission):
        """
        """
        raise NotImplementedError("%s must implement remove_permission method" % self)

    def remove_all_permissions_of_resource(self, resource):
        """
        """
        raise NotImplementedError("%s must implement remove_all_permissions_of_resource method" % self)

    def remove_all_permissions_for_target_ids(self, target_ids):
        """
        """
        raise NotImplementedError("%s must implement remove_all_permissions_for_target_ids method" % self)

    def has_permission(self, resource, target, permission, explicit_only=False):
        """
        """
        raise NotImplementedError("%s must implement has_permission method" % self)

    def child_ids_with_permission(self, resource, parent, children_type, permission=None):
        """
        """
        raise NotImplementedError("%s must implement child_ids_with_permission method" % self)

    def is_empty(self):
        """
        """
        raise NotImplementedError("%s must implement is_empty method" % self)
