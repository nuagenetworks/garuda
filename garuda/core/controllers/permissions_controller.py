# -*- coding: utf-8 -*-

import logging
from uuid import uuid4

from garuda.core.models import GAPluginController
from garuda.core.plugins import GAPermissionsPlugin

logger = logging.getLogger('garuda.controller.authentication')



class GAPermissionsController(GAPluginController):
    """
    """

    def __init__(self, plugins, core_controller):
        """
        """
        super(GAPermissionsController, self).__init__(core_controller=core_controller, plugins=plugins)
        self._managing_plugin_registry = {}

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.permissions'

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        return GAPermissionsPlugin

    # API

    def _managing_plugin(self):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage():
                return plugin

        return None  # pragma: no cover


    def create_permission(self, resource, target, permission, explicit=True, parent_permission_id=None):
        """
        """
        plugin = self._managing_plugin()
        return plugin.create_permission(resource=resource, target=target, permission=permission, explicit=explicit, parent_permission_id=parent_permission_id) if plugin else None

    def remove_permission(self, resource, target, permission):
        """
        """
        plugin = self._managing_plugin()
        return plugin.remove_permission(resource=resource, target=target, permission=permission) if plugin else None

    def remove_all_permissions_of_resource(self, resource):
        """
        """
        plugin = self._managing_plugin()
        return plugin.remove_all_permissions_of_resource(resource=resource) if plugin else None

    def remove_all_permissions_for_target_ids(self, target_ids):
        """
        """
        plugin = self._managing_plugin()
        return plugin.remove_all_permissions_for_target_ids(target_ids=target_ids) if plugin else None

    def has_permission(self, resource, target, permission, explicit_only=False):
        """
        """
        plugin = self._managing_plugin()
        return plugin.has_permission(resource=resource, target=target, permission=permission, explicit_only=explicit_only) if plugin else None

    def child_ids_with_permission(self, resource, parent, children_type, permission=None):
        """
        """
        plugin = self._managing_plugin()
        return plugin.child_ids_with_permission(resource=resource, parent=parent, children_type=children_type, permission=permission) if plugin else None

    def is_empty(self):
        """
        """
        plugin = self._managing_plugin()
        return plugin.is_empty() if plugin else True
