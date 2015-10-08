# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('Garuda.plugins.AuthenticationController')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAPermissionsControllerPlugin


class PermissionsController(GAPluginController):
    """

    """
    def __init__(self, plugins):
        """
        """
        super(PermissionsController, self).__init__(plugins=plugins)

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(PermissionsController, self).register_plugin(plugin=plugin, plugin_type=GAPermissionsControllerPlugin)

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
