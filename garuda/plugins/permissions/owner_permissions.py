# -*- coding: utf-8 -*-

import logging

from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GAPermissionsPlugin
from garuda.core.lib import GASDKLibrary

logger = logging.getLogger('garuda.controller.permission.simple')


class GAOwnerPermissionsPlugin(GAPermissionsPlugin):
    """
    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='owner_permissions', version=1.0, identifier='garuda.controller.permissions.owner')

    def should_manage(self):
        """
        """
        return True

    # API

    def create_permission(self, resource, target, permission, explicit=True, parent_permission_id=None):  # pragma: no cover
        """
        """
        pass

    def remove_permission(self, resource, target, permission):  # pragma: no cover
        """
        """
        pass

    def remove_all_permissions_of_resource(self, resource):  # pragma: no cover
        """
        """
        pass

    def remove_all_permissions_for_target_ids(self, target_ids):  # pragma: no cover
        """
        """
        pass

    def has_permission(self, resource, target, permission, explicit_only=False):
        """
        """
        return target.owner == resource

    def child_ids_with_permission(self, resource, parent, children_type, permission=None):
        """
        """
        return '__OWNER_ONLY__'

    # Utilities

    def is_empty(self):
        """
        """
        return False