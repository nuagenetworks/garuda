# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('garuda.controller.authentication')

from garuda.core.models import GAPluginController
from garuda.core.plugins import GAPermissionsPlugin


class GAPermissionsController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GAPermissionsController, self).__init__(core_controller=core_controller, plugins=plugins)

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.authentication'

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        return GAPermissionsPlugin

    # Implementation

    def create_permission(self, resource, target, action, implicit=False):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource=resource, target=target, action=action):
                return plugin.create_permission(resource=resource, target=target, action=action, implicit=implicit)

        return None

    def remove_permission(self, resource, target, action):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource=resource, target=target, action=action):
                return plugin.remove_permission(resource=resource, target=target, action=action)

        return None

    def has_permission(self, resource, target, action):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource=resource, target=target, action=action):
                return plugin.has_permission(resource=resource, target=target, action=action)

        return None
