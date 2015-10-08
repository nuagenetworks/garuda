# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('Garuda.ModelController')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAModelControllerPlugin


class ModelController(GAPluginController):
    """

    """
    def __init__(self, plugins):
        """
        """
        super(ModelController, self).__init__(plugins=plugins)

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(ModelController, self).register_plugin(plugin=plugin, plugin_type=GAModelControllerPlugin)

    # Implementation

    def instantiate(self, resource_name):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=None):
                return plugin.instantiate(resource_name=resource_name)

        return None

    def get(self, resource_name, identifier):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=identifier):
                return plugin.get(resource_name=resource_name, identifier=identifier)

        return None

    def get_all(self, parent, resource_name):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=None):
                return plugin.get_all(parent=parent, resource_name=resource_name)

        return None

    def save(self, resource, parent=None):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource.rest_resource_name, identifier=resource.id):
                return plugin.save(resource=resource, parent=parent)

        return None

    def delete(self, resource):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource.rest_resource_name, identifier=resource.id):
                return plugin.delete(resource=resource)

        return None
